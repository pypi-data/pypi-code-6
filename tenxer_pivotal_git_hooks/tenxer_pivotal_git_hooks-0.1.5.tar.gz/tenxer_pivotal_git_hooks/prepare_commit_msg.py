import sys

from tenxer_pivotal_git_hooks import utils


def validate_story_id(story_id):
    pass


def add_story_id_to_message():
    filename = sys.argv[1]
    with open(filename, 'r') as message_file:
        commit_msg = message_file.read()

    branch_name = utils.execute_cmd("git rev-parse --abbrev-ref HEAD")
    story_id = branch_name.split('-')[-1]
    template = '{{story_id}}'
    try:
        story_id = int(story_id)
        story_id_reference = '#{story_id}'.format(story_id=story_id)
        if story_id_reference not in commit_msg:
            story_ref = '[Finishes #{story_id}]'.format(story_id=story_id)
            if template in commit_msg:
                commit_msg = commit_msg.replace(template, story_ref)
            else:
                commit_msg = '{}\n{}'.format(commit_msg, story_ref)
    except ValueError:
        if template in commit_msg:
            commit_msg = commit_msg.replace(template, '')

    with open(filename, 'w') as message_file:
        message_file.write(commit_msg)
