import json
import sys

from tenxer_pivotal_git_hooks import api, utils


def is_branch_author(branch_name):
    cmd = (
        "git log {branch_name} "
        "--not $(git for-each-ref "
        "--format='%(refname)' refs/heads/ "
        "| grep -v 'refs/heads/{branch_name}') "
        "--pretty='%an'"
    ).format(branch_name=branch_name)
    commit_authors = utils.execute_cmd(cmd)
    if commit_authors:
        git_user_name = utils.execute_cmd('git config user.name')
        is_author = commit_authors.startswith(git_user_name)
    else:
        is_author = True
    return is_author


def is_valid_branch(branch_name):
    return (
        not branch_name.startswith(("master", "origin", "HEAD"))
        and is_branch_author(branch_name)
    )


def get_story_selection(projects, account_id):
    if not utils.is_screen_available():
        print "Unable to get input so not able to show story selections."
        return

    stories = []
    for project in projects:
        project_id = project['project_id']
        path = 'projects/{}/stories'.format(project_id)
        params = {
            'filter': 'state:unscheduled,unstarted,started,rejected'
        }
        response = api.request_url('get', path, params=params)
        stories = json.loads(response.content)
        stories = sorted(
            stories, key=lambda s: s.get('owned_by_id') == account_id,
            reverse=True)
        for start_of_range in range(0, len(stories), 10):
            output = (
                "Enter a number to associate this branch to a story.\n"
                "To see more stories hit enter.\n"
                "To skip enter S.\n")
            for num, story in (
                    enumerate(stories[start_of_range:start_of_range + 10])):
                index = start_of_range + num
                output += '[{}] {}\n'.format(index, story.get('name'))
            story_number = raw_input(output).strip()
            try:
                story = stories[int(story_number)]
                story_id = story['id']
                return story_id
            except ValueError:
                if story_number == "S":
                    return None


def transition_story(projects, story_id, state, account_id, extra_data=None):
    success = False
    try:
        story_id = int(story_id)
        for project in projects:
            project_id = project['project_id']
            path = 'projects/{project_id}/stories/{story_id}'.format(
                project_id=project_id, story_id=story_id)
            data = {
                'current_state': state,
                'owned_by_id': [account_id],
            }
            if extra_data:
                data.update(extra_data)
            response = api.request_url('put', path, data=data)
            if response.status_code == 400:
                error = json.loads(response.content)
                validation_errors = error.get('validation_errors') or []
                for validation_error in validation_errors:
                    if validation_error.get('field') == 'estimate':
                        if utils.is_screen_available():
                            message = (
                                'Please provide an estimate for the story:\n')
                            estimate = utils.get_input(message)
                            if not extra_data:
                                extra_data = {}
                            extra_data['estimate'] = int(estimate)
                            return transition_story(
                                projects, story_id, state, account_id,
                                extra_data=extra_data)
                        else:
                            print (
                                'Story needs an estimate before it can be '
                                'started.')
                            return
            if response.status_code == 200:
                story = json.loads(response.content)
                print "{} story {}".format(state, story.get('name'))
                success = True
                break
    except ValueError:
        print "Unable to find a story id"

    if not success:
        print "Unable to find story {}".format(story_id)


def comment_on_story(projects, story_id, comment):
    try:
        story_id = int(story_id)
        for project in projects:
            project_id = project['project_id']
            path = 'projects/{project_id}/stories/{story_id}/comments'.format(
                project_id=project_id, story_id=story_id)
            data = {'text': comment}
            response = api.request_url('post', path, data=data)
            if response.status_code == 200:
                break
    except ValueError:
        print "Unable to add comment because to story could not be found"


def update_branch_story():
    is_branch = sys.argv[3]
    if not is_branch:
        return

    response = api.request_url('get', 'me')
    account = json.loads(response.content)
    projects = account.get('projects')
    account_id = account.get('id')

    started_branch = utils.execute_cmd("git rev-parse --abbrev-ref HEAD")
    started_story_id = started_branch.split('-')[-1].strip()
    if is_valid_branch(started_branch):
        try:
            started_story_id = int(started_story_id)
        except ValueError:
            started_story_id = get_story_selection(projects, account_id)
            if started_story_id:
                new_branch_name = '{}-{}'.format(
                    started_branch, started_story_id)
                update_branch_name_cmd = "git branch -m {} {}".format(
                    started_branch, new_branch_name)
                utils.execute_cmd(update_branch_name_cmd)

        if started_story_id:
            transition_story(projects, started_story_id, 'started', account_id)
    elif started_branch != "master":
        try:
            started_story_id = int(started_story_id)
            comment_on_story(projects, started_story_id, 'Reviewing')
        except ValueError:
            pass

    unstarted_branch = utils.execute_cmd("git rev-parse --abbrev-ref @{-1}")
    unstarted_story_id = unstarted_branch.split('-')[-1].strip()
    if is_valid_branch(unstarted_branch):
        if unstarted_story_id and unstarted_story_id != started_story_id:
            transition_story(
                projects, unstarted_story_id, 'unstarted', account_id)
    elif unstarted_branch != "master":
        try:
            unstarted_story_id = int(unstarted_story_id)
            comment_on_story(
                projects, unstarted_story_id, 'No longer reviewing')
        except ValueError:
            pass
