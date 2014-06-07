
OVERVIEW = """\
-   Overview
    -   Sample entries
    -   Starting etm
    -   Views
    -   Creating New Items
    -   Editing Existing Items
    -   Idle Time
    -   Tools
    -   Data Organization and Calendars

Overview
========

In contrast to most calendar/todo applications, creating items (events, tasks, and so forth) in etm does not require filling out fields in a form. Instead, items are created as free-form text entries using a simple, intuitive format and stored in plain text files.

Dates in the examples below are entered using fuzzy parsing - e.g., +7 for seven days from today, fri for the first Friday on or after today, +1/1 for the first day of next month, sun - 6d for Monday of the current week. See Dates for details.

Sample entries
--------------

-   A sales meeting (an event) [s]tarting seven days from today at 9:00am with an [e]xtent of one hour and a default [a]lert 5 minutes before the start:

        * sales meeting @s +7 9a @e 1h @a 5

-   The sales meeting with another [a]lert 2 days before the meeting to (e)mail a reminder to a list of recipients:

        * sales meeting @s +7 9a @e 1h @a 5
          @a 2d: e; who@when.com, what@where.org

-   Prepare a report (a task) for the sales meeting [b]eginning 3 days early:

        - prepare report @s +7 @b 3

-   A period [e]xtending 35 minutes (an action) spent working on the report yesterday:

        ~ report preparation @s -1 @e 35

-   Get a haircut (a task) on the 24th of the current month and then [r]epeatedly at (d)aily [i]ntervals of (14) days and, [o]n completion, (r)estart from the completion date:

        - get haircut @s 24 @r d &i 14 @o r

-   Payday (an occasion) on the last week day of each month. The &s -1 part of the entry extracts the last date which is both a weekday and falls within the last three days of the month):

        ^ payday @s 1/1 @r m &w MO, TU, WE, TH, FR
          &m -1, -2, -3 &s -1

-   Take a prescribed medication daily (a reminder) [s]tarting today and [r]epeating (d)aily at [h]ours 10am, 2pm, 6pm and 10pm [u]ntil (12am on) the fourth day from today. Trigger the default [a]lert zero minutes before each reminder:

        * take Rx @s +0 @r d &h 10, 14, 18, 22 &u +4 @a 0

-   Move the water sprinkler (a reminder) every thirty mi[n]utes on Sunday afternoons using the default alert zero minutes before each reminder:

        * Move sprinkler @s 1 @r w &w SU &h 14, 15, 16, 17 &n 0, 30 @a 0

    To limit the sprinkler movement reminders to the [M]onths of April through September each year change the @r entry to this:

        @r w &w SU &h 14, 15, 16, 17 &n 0, 30 &M 4, 5, 6, 7, 8, 9

    or this:

        @r n &i 30 &w SU &h 14, 15, 16, 17 &M 4, 5, 6, 7, 8, 9

-   Presidential election day (an occasion) every four years on the first Tuesday after a Monday in November:

        ^ Presidential Election Day @s 2012-11-06
          @r y &i 4 &M 11 &m 2, 3, 4, 5, 6, 7, 8 &w TU

-   Join the etm discussion group (a task) [s]tarting 14 days from today. Because of the @g (goto) link, pressing G when this item is selected in the gui would open the link using the system default application which, in this case, would be your default browser:

        - join the etm discussion group @s +14
          @g groups.google.com/group/eventandtaskmanager/topics

Starting etm
------------

To start the etm GUI open a terminal window and enter etm at the prompt:

    $ etm

If you have not done a system installation of etm you will need first to cd to the directory where you unpacked etm.

You can add a command to use the CLI instead of the GUI. For example, to get the complete command line usage information printed to the terminal window just add a question mark:

    $ etm ?
    Usage:

        etm [logging level] [path] [?] [acmsv]

    With no arguments, etm will set logging level 3 (warn), use settings from
    the configuration file ~/.etm/etmtk.cfg, and open the GUI.

    If the first argument is an integer not less than 1 (debug) and not greater
    than 5 (critical), then set that logging level and remove the argument.

    If the first (remaining) argument is the path to a directory that contains
    a file named etmtk.cfg, then use that configuration file and remove the
    argument.

    If the first (remaining) argument is one of the commands listed below, then
    execute the remaining arguments without opening the GUI.

        a ARG   display the agenda view using ARG, if given, as a filter.
        c ARGS  display a custom view using the remaining arguments as the
                specification. (Enclose ARGS in single quotes to prevent shell
                expansion.)
        d ARG   display the day view using ARG, if given, as a filter.
        k ARG   display the keywords view using ARG, if given, as a filter.
        m INT   display a report using the remaining argument, which must be a
                positive integer, to display a report using the corresponding
                entry from the file given by report_specifications in etmtk.cfg.
                Use ? m to display the numbered list of entries from this file.
        n ARG   display the notes view using ARG, if given, as a filter.
        N ARGS  Create a new item using the remaining arguments as the item
                specification. (Enclose ARGS in single quotes to prevent shell
                expansion.)
        p ARG   display the path view using ARG, if given, as a filter.
        t ARG   display the tags view using ARG, if given, as a filter.
        v       display information about etm and the operating system.
        ? ARG   display (this) command line help information if ARGS = '' or,
                if ARGS = X where X is one of the above commands, then display
                details about command X. 'X ?' is equivalent to '? X'.

For example, you can print your agenda to the terminal window by adding the letter "a":

    $ etm a
    Sun Apr 06, 2014
      > set up luncheon meeting with Joe Smith           4d
    Mon Apr 07, 2014
      * test command line event                      3pm ~ 4pm
      * Aerobics                                     5pm ~ 6pm
      - follow up with Mary Jones
    Wed Apr 09, 2014
      * Aerobics                                     5pm ~ 6pm
    Thu Apr 10, 2014
      * Frank Burns conference call 1pm Pacif..     4pm ~ 5:30pm
      * Book club                                    7pm ~ 9pm
      - sales meeting
      - set up luncheon meeting with Joe Smith          15m
    Now
      Available
        - Hair cut                                      -1d
    Next
      errands
        - milk and eggs
      phone
        - reservation for Saturday dinner
    Someday
      ? lose weight and exercise more

You can filter the output by adding a (case-insensitive) argument:

    $ etm a smith
    Sun Apr 06, 2014
      > set up luncheon meeting with Joe Smith           4d
    Thu Apr 10, 2014
      - set up luncheon meeting with Joe Smith          15m

or etm d mar .*2014 to show your items for March, 2014.

You can add a question mark to a command to get details about the commmand, e.g.:

    Usage:

        etm c <type> <groupby> [options]

    Generate a custom view where type is either 'a' (action) or 'c' (composite).
    Groupby can include *semicolon* separated date specifications and
    elements from:
        c context
        f file path
        k keyword
        t tag
        u user

    A *date specification* is either
        w:   week number
    or a combination of one or more of the following:
        yy:   2-digit year
        yyyy:   4-digit year
        MM:   month: 01 - 12
        MMM:   locale specific abbreviated month name: Jan - Dec
        MMMM:   locale specific month name: January - December
        dd:   month day: 01 - 31
        ddd:   locale specific abbreviated week day: Mon - Sun
        dddd:   locale specific week day: Monday - Sunday

    Options include:
        -b begin date
        -c context regex
        -d depth (CLI a reports only)
        -e end date
        -f file regex
        -k keyword regex
        -l location regex
        -o omit (r reports only)
        -s summary regex
        -S search regex
        -t tags regex
        -u user regex
        -w column 1 width
        -W column 2 width

    Example:

        etm c 'c ddd, MMM dd yyyy -b 1 -e +1/1'

Note: The CLI offers the same views and reporting, with the exception of week view, as the GUI. It is also possible to create new items in the CLI with the n command. Other modifications such as copying, deleting, finishing and so forth, can only be done in the GUI or, perhaps, in your favorite text editor. An advantage to using the GUI is that it provides validation.

Tip: If you have a terminal open, you can create a new item or put something to finish later in your inbox quickly and easily with the "i" command. For example,

        etm i '123 456-7890'

would create an entry in your inbox with this phone number. (With no type character an "$" would be supplied automatically to make the item an inbox entry and no further validation would be done.)

Views
-----

All views, including week view, display only items consistent with the current choices of active calendars.

If a (case-insensitive) filter is entered then the display in all views other than week view and custom view will be limited to items that match somewhere in either the branch or the leaf. Relevant branches will automatically be expanded to show matches.

In day and week views, pressing the space bar will move the display to the current date. In all other views, pressing the space bar will move the display to the first item in the outline.

In day and week views, pressing J will first prompt for a fuzzy-parsed date and then "jump" to the specified date.

If you scroll or jump to a date in either day view or week view and then open the other view, the same day(s) will be displayed.

In all views, pressing Return with an item selected or double clicking an item or a busy period in week view will open a context menu with options to copy, delete, edit and so forth.

In all views, clicking in the details panel with an item selected will open the item for editing if it is not repeating and otherwise prompt for the instance(s) to be changed.

In all views other than week view, pressing O will open a dialog to choose the outline depth.

In all views other than week view, pressing L will toggle the display of a column displaying item labels where, for example, an item with @a, @d and @u fields would have the label "adu".

In all views other than week view, pressing S will show a text verion of the current display suitable for copy and paste. The text version will respect the current outline depth in the view.

In custom view it is possible to export the current report in either text or CSV (comma separated values) format to a file of your choosing.

Note. In custom view you need to remove the focus from the report specification entry field in order for the shortcuts O, L and S to work.

In all views other than custom view and week view:

-   if an item is selected:

    -   pressing Shift-H will show a history of changes for the file containing the selected item, first prompting for the number of changes.

    -   pressing Shift-X will export the selected item in iCal format.

-   if an item is not selected:

    -   pressing Shift-H will show a history of changes for all files, first prompting for the number of changes.

    -   pressing Shift-X will export all items in active calendars in iCal format.

Agenda View

What you need to know now beginning with your schedule for the next few days and followed by items in these groups:

-   In basket: In basket items and items with missing types or other errors.

-   Now: All scheduled (dated) tasks whose due dates have passed including delegated tasks and waiting tasks (tasks with unfinished prerequisites) grouped by available, delegated and waiting and, within each group, by the due date.

-   Next: All unscheduled (undated) tasks grouped by context (home, office, phone, computer, errands and so forth) and sorted by priority and extent. These tasks correspond to GTD's next actions. These are tasks which don't really have a deadline and can be completed whenever a convenient opportunity arises. Check this view, for example, before you leave to run errands for opportunities to clear other errands.

-   Someday: Someday (maybe) items for periodic review.

Note: Finished tasks, actions and notes are not displayed in this view.

Day View

All dated items appear in this view, grouped by date and sorted by starting time and item type. This includes:

-   All non-repeating, dated items.

-   All repetitions of repeating items with a finite number of repetitions. This includes 'list-only' repeating items and items with &u (until) or &t (total number of repetitions) entries.

-   For repeating items with an infinite number of repetitions, those repetitions that occur within the first weeks_after weeks after the current week are displayed along with the first repetition after this interval. This assures that at least one repetition will be displayed for infrequently repeating items such as voting for president.

Tip: Want to see your next appointment with Dr. Jones? Switch to day view and enter "jones" in the filter.

Week View

Events and occasions displayed graphically by week. Left and right cursor keys change, respectively, to the previous and next week. Up and down cursor keys select, respectively, the previous and next items within the given week. Items can also be selected by moving the mouse over the item. The details for the selected item are displayed at the bottom of the screen. Pressing return with an item selected or double-clicking an item opens a context menu. Control-clicking an unscheduled time opens a dialog to create an event for that date and time.

Tip. You can display a list of busy times or, after providing the needed period in minutes, a list of free times that would accomodate the requirement within the selected week. Both options are in the View menu.

Month View

Events and occasions displayed graphically by month. Left and right cursor keys change, respectively, to the previous and next month. Up and down cursor keys select, respectively, the previous and next days within the given month. Days can also be selected by moving the mouse over the item. A list of occasions and events for the selected day is displayed at the bottom of the screen.

The current date and days with occasions are highlighted and day numbers are colored in shades ranging from black to red to reflect the time scheduled for events in the day.

Tip. You can display a list of busy times or, after providing the needed period in minutes, a list of free times that would accomodate the requirement within the selected month. Both options are in the View menu.

Tag View

All items with tag entries grouped by tag and sorted by type and relevant datetime. Note that items with multiple tags will be listed under each tag.

Tip: Use the filter to limit the display to items with a particular tag.

Keyword View

All items grouped by keyword and sorted by type and relevant datetime.

Path View

All items grouped by file path and sorted by type and relevant datetime. Use this view to review the status of your projects.

The relevant datetime is the past due date for any past due task, the starting datetime for any non-repeating item and the datetime of the next instance for any repeating item.

Note: Items that you have "commented out" by beginning the item with a # will only be visible in this view.

Note View

All notes grouped and sorted by keyword and summary.

Custom View

Design your own view. See Reports for details.

Creating New Items
------------------

Items of any type can be created by pressing N in the GUI and then providing the details for the item in the resulting dialog.

An event can also be created by double-clicking in a free period in the Week View - the date and time corresponding to the mouse position will be entered as the starting datetime when the dialog opens.

An action can also be created by pressing T to start a timer for the action. You will be prompted for a summary (title) and, optionally, an @e entry to specify a starting time for the timer. If an item is selected when you press T then you will have the additional option of creating the action as a copy of the selected item.

The timer starts automatically when you close the dialog. Once the timer is running, pressing T toggles the timer between running and paused. Pressing Shift-T when a timer is active (either running or paused) stops the timer and begins a dialog to provide the details of the action - the elapsed time will already be entered.

While a timer is active, the title, elapsed time and status - running or paused - is displayed in the status bar.

When editing an item, clicking on Finish or pressing Shift-Return will validate your entry. If there are errors, they will be displayed and you can return to the editor to correct them. If there are no errors, this will be indicated in a dialog, e.g.,

    Task scheduled for Tue Jun 03

    Save changes and exit?

Tip. When creating or editing a repeating item, pressing Finish will also display a list of instances that will be generated.

Click on Ok or press Return or Shift-Return to save the item and close the editor. Click on Cancel or press Escape to return to the editor.

If this is a new item and there are no errors, clicking on Ok or pressing Return will open a dialog to select the file to store the item with the current monthly file already selected. Pressing Shift-Return will bypass the file selection dialog and save to the current monthly file.

Editing Existing Items
----------------------

Double-clicking an item or pressing Return when an item is selected will open a context menu of possible actions:

-   Copy
-   Delete
-   Edit
-   Edit file
-   Finish (unfinished tasks only)
-   Reschedule
-   Schedule new
-   Open link (items with @g entries only)
-   Show user details (items with @u entries only)

When either Copy or Edit is chosen for a repeating item, you can further choose:

1.  this instance
2.  this and all subsequent instances
3.  all instances

When Delete is chosen for a repeating item, a further choice is available:

4.  all previous instances

Tip: Use Reschedule to enter a date for an undated item or to change the scheduled date for the item or the selected instance of a repeating item. All you have to do is enter the new (fuzzy parsed) datetime.

Idle Time
---------

Idle timing is also supported. An illustrative work flow would be to activate the idle timer first thing each morning by pressing I. The current value of this timer will then be displayed in brackets in the lower, left-hand corner of the GUI.

If you later start an action timer, a dialog will open showing the current idle time and offering the opportunity to assign some or all of this period to a keyword that you select from a list. You can continue assigning time in this fashion until idle time is zero or you can press Cancel or Escape at any point to cancel the dialog and open the action timer dialog. While the action timer is running, the idle timer will be paused and vice-versa.

If an action timer is canceled (stopped and not recorded), then the time for the action timer will be added to the current idle time.

You can assign idle time without starting an action timer by pressing I or, at the end of the day, by pressing Shift-I to stop the idle timer.

Note that the dialog to assign idle time will only open when starting or restarting an action timer if the current idle time is at least the number of minutes specified by idle_minimum in your etmtk.cfg file.

Tools
-----

Date and time calculator

Enter an expression of the form x [+-] y where x is a date and y is either a date or a time period if - is used and a time period if + is used. Both x and y can be followed by timezones, e.g.,

     4/20 6:15p US/Central - 4/20 4:50p Asia/Shanghai:

     14h25m

or

     4/20 4:50p Asia/Shanghai + 14h25m US/Central:

     2014-04-20 18:15-0500

The local timezone is assumed when none is given.

Available dates calculator

Enter an expression of the form

    start; end; busy

where start and end are dates and busy is comma separated list of busy dates or busy intervals. E.g., entering

    6/1; 6/30; 6/2, 6/14-6/22, 6/5-6/9, 6/11-6/15, 6/17-6/29

would give:

    Sun Jun 01
    Tue Jun 03
    Wed Jun 04
    Tue Jun 10
    Mon Jun 30

Yearly calendar

Gives a display such as

          January 2014           February 2014             March 2014
      Mo Tu We Th Fr Sa Su    Mo Tu We Th Fr Sa Su    Mo Tu We Th Fr Sa Su
             1  2  3  4  5                    1  2                    1  2
       6  7  8  9 10 11 12     3  4  5  6  7  8  9     3  4  5  6  7  8  9
      13 14 15 16 17 18 19    10 11 12 13 14 15 16    10 11 12 13 14 15 16
      20 21 22 23 24 25 26    17 18 19 20 21 22 23    17 18 19 20 21 22 23
      27 28 29 30 31          24 25 26 27 28          24 25 26 27 28 29 30
                                                      31

           April 2014               May 2014               June 2014
      Mo Tu We Th Fr Sa Su    Mo Tu We Th Fr Sa Su    Mo Tu We Th Fr Sa Su
          1  2  3  4  5  6              1  2  3  4                       1
       7  8  9 10 11 12 13     5  6  7  8  9 10 11     2  3  4  5  6  7  8
      14 15 16 17 18 19 20    12 13 14 15 16 17 18     9 10 11 12 13 14 15
      21 22 23 24 25 26 27    19 20 21 22 23 24 25    16 17 18 19 20 21 22
      28 29 30                26 27 28 29 30 31       23 24 25 26 27 28 29
                                                      30

           July 2014              August 2014            September 2014
      Mo Tu We Th Fr Sa Su    Mo Tu We Th Fr Sa Su    Mo Tu We Th Fr Sa Su
          1  2  3  4  5  6                 1  2  3     1  2  3  4  5  6  7
       7  8  9 10 11 12 13     4  5  6  7  8  9 10     8  9 10 11 12 13 14
      14 15 16 17 18 19 20    11 12 13 14 15 16 17    15 16 17 18 19 20 21
      21 22 23 24 25 26 27    18 19 20 21 22 23 24    22 23 24 25 26 27 28
      28 29 30 31             25 26 27 28 29 30 31    29 30

          October 2014           November 2014           December 2014
      Mo Tu We Th Fr Sa Su    Mo Tu We Th Fr Sa Su    Mo Tu We Th Fr Sa Su
             1  2  3  4  5                    1  2     1  2  3  4  5  6  7
       6  7  8  9 10 11 12     3  4  5  6  7  8  9     8  9 10 11 12 13 14
      13 14 15 16 17 18 19    10 11 12 13 14 15 16    15 16 17 18 19 20 21
      20 21 22 23 24 25 26    17 18 19 20 21 22 23    22 23 24 25 26 27 28
      27 28 29 30 31          24 25 26 27 28 29 30    29 30 31

Left and right cursor keys move backward and forward a year at a time, respectively, and pressing the spacebar returns to the current year.

History of changes

This requires that either git or mercurial is installed. If an item is selected show a history of changes to the file that contains the item. Otherwise show a history of changes for all etm data files. In either case, choose an integer number of the most recent changes to show or choose 0 to show all changes.

Export to iCal

If an item is selected, export the item in iCalendar format to the file given by icsitem_file in your etmtk.cfg. Otherwise, export active calendars in iCalendar format to the file given by icscal_file.

Data Organization and Calendars
-------------------------------

etm offers two hierarchical ways of organizing your data: by keyword and file path. There are no hard and fast rules about how to use these hierarchies but the goal is a system that makes complementary uses of folder and keyword and fits your needs. As with any filing system, planning and consistency are paramount.

For example, one pattern of use for a business would be to use folders for people and keywords for client-project-category.

Similarly, a family could use folders to separate personal and shared items for family members, for example:

    root etm data directory
        personal
            dag
            erp
        shared
            holidays
            birthdays
            events

Here

    ~dag/.etm/etm.cfg
    ~erp/.etm/etm.cfg

would both contain datadir entries specifying the common root data directory. Additionally, if these configuration files contained, respectively, the entries

    ~dag/.etm/etm.cfg
        calendars
        - [dag, true, personal/dag]
        - [erp, false, personal/erp]
        - [shared, true, shared]

and

    ~erp/.etm/etm.cfg
        calendars
        - [erp, true, personal/erp]
        - [dag, false, personal/dag]
        - [shared, true, shared]

then, by default, both dag and erp would see the entries from their personal files as well as the shared entries and each could optionally view the entries from the other's personal files as well. See the Preferences for details on the calendars entry.

Note for Windows users. The path separator needs to be "escaped" in the calendar paths, e.g., you should enter

     - [dag, true, personal\\dag]

instead of

     - [dag, true, personal\dag]
"""

ITEMTYPES = """\
-   Items
    -   \~ Action
    -   \* Event
    -   \^ Occasion
    -   ! Note
    -   - Task
    -   % Delegated task
    -   + Task group
    -   \$ In basket
    -   ? Someday maybe
    -   \# Hidden
    -   = Defaults

Items
=====

There are several types of items in etm. Each item begins with a type character such as an asterisk (event) and continues on one or more lines either until the end of the file is reached or another line is found that begins with a type character. The type character for each item is followed by the item summary and then, perhaps, by one or more @key value pairs - see @-Keys for details. The order in which such pairs are entered does not matter.

~ Action
--------

A record of the expenditure of time (@e) and/or money (@x). Actions are not reminders, they are instead records of how time and/or money was actually spent. Action lines begin with a tilde, ~.

        ~ picked up lumber and paint @s mon 3p @e 1h15m @x 127.32

Entries such as @s mon 3p, @e 1h15m and @x 127.32 are discussed below under Item details. Action entries form the basis for time and expense billing using action reports - see Reports for details.

Tip: You can use either path or keyword or a combination of the two to organize your actions.

* Event
-------

Something that will happen on particular day(s) and time(s). Event lines begin with an asterick, *.

        * dinner with Karen and Al @s sat 7p @e 3h

Events have a starting datetime, @s and an extent, @e. The ending datetime is given implicitly as the sum of the starting datetime and the extent. Events that span more than one day are possible, e.g.,

        * Sales conference @s 9a wed @e 2d8h

begins at 9am on Wednesday and ends at 5pm on Friday.

An event without an @e entry or with @e 0 is regarded as a reminder and, since there is no extent, will not be displayed in busy times.

^ Occasion
----------

Holidays, anniversaries, birthdays and such. Similar to an event with a date but no starting time and no extent. Occasions begin with a caret sign, ^.

        ^ The !1776! Independence Day @s 2010-07-04 @r y &M 7 &m 4

On July 4, 2013, this would appear as The 237th Independence Day. Here !1776!` is an example of an anniversary substitution - see Dates for details.

! Note
------

A record of some useful information. Note lines begin with an exclamation point, !.

    ! xyz software @k software:passwords @d user: dnlg, pw: abc123def

Tip: Since both the GUI and CLI note views group and sort by keyword, it is a good idea to use keywords to organize your notes.

- Task
------

Something that needs to be done. It may or may not have a due date. Task lines begin with a minus sign, -.

    - pay bills @s Oct 25

A task with an @s entry becomes due on that date and past due when that date has passed. If the task also has an @b begin-by entry, then advance warnings of the task will begin appearing the specified number of days before the task is due. An @e entry in a task is interpreted as an estimate of the time required to finish the task.

% Delegated task
----------------

A task that is assigned to someone else, usually the person designated in an @u entry. Delegated tasks begin with a percent sign, %.

        % make reservations for trip @u joe @s fri

+ Task group
------------

A collection of related tasks, some of which may be prerequisite for others. Task groups begin with a plus sign, +.

        + dog house
          @j pickup lumber and paint      &q 1
          @j cut pieces                   &q 2
          @j assemble                     &q 3
          @j paint                        &q 4

Note that a task group is a single item and is treated as such. E.g., if any job is selected for editing then the entire group is displayed.

Individual jobs are given by the @j entries. The queue entries, &q, set the order --- tasks with smaller &q values are prerequisites for subsequent tasks with larger &q values. In the example above, neither "pickup lumber" nor "pickup paint" have any prerequisites. "Pickup lumber", however, is a prerequisite for "cut pieces" which, in turn, is a prerequisite for "assemble". Both "assemble" and "pickup paint" are prerequisites for "paint".

$ In basket
-----------

A quick, don't worry about the details item to be edited later when you have the time. In basket entries begin with a dollar sign, $.

        $ joe 919 123-4567

If you create an item using etm and forget to provide a type character, an $ will automatically be inserted.

? Someday maybe
---------------

Something are you don't want to forget about altogether but don't want to appear on your next or scheduled lists. Someday maybe items begin with a question mark, ?.

        ? lose weight and exercise more

# Hidden
--------

Hidden items begin with a hash mark, #. Such items are ignored by etm save for appearing in the folder view. Stick a hash mark in front of any item that you don't want to delete but don't want to see in your other views.

= Defaults
----------

Default entries begin with an equal sign, =. These entries consist of @key value pairs which then become the defaults for subsequent entries in the same file until another = entry is reached.

Suppose, for example, that a particular file contains items relating to "project_a" for "client_1". Then entering

    = @k client_1:project_a

on the first line of the file and

    =

on the twentieth line of the file would set the default keyword for entries between the first and twentieth line in the file.
"""

ATKEYS = """\
-   @-Keys
    -   @a alert
    -   @b beginby
    -   @c context
    -   @d description
    -   @e extent
    -   @f done[; due]
    -   @g goto
    -   @h history
    -   @j job
    -   @k keyword
    -   @l location
    -   @m memo
    -   @o overdue
    -   @p priority
    -   @r repetition rule
    -   @s starting datetime
    -   @t tags
    -   @u user
    -   @v action\_rates key
    -   @w action\_markups key
    -   @x expense
    -   @z time zone
    -   @+ include
    -   @- exclude

@-Keys
======

@a alert
--------

The specification of the alert(s) to use with the item. One or more alerts can be specified in an item. E.g.,

    @a 10m, 5m
    @a 1h: s

would trigger the alert(s) specified by default_alert in your etm.cfg at 10 and 5 minutes before the starting time and a (s)ound alert one hour before the starting time.

The alert

    @a 2d: e; who@what.com, where2@when.org; filepath1, filepath2

would send an email to the two listed recipients exactly 2 days (48 hours) before the starting time of the item with the item summary as the subject, with file1 and file2 as attachments and with the body of the message composed using email_template from your etm.cfg.

Similarly, the alert

    @a 10m: t; 9191234567@vtext.com, 9197654321@txt.att.net

would send a text message 10 minutes before the starting time of the item to the two mobile phones listed (using 10 digit area code and carrier mms extension) together with the settings for sms in etm.cfg. If no numbers are given, the number and mms extension specified in sms.phone will be used. Here are the mms extensions for the major US carriers:

    Alltel          @message.alltel.com
    AT&T            @txt.att.net
    Nextel          @messaging.nextel.com
    Sprint          @messaging.sprintpcs.com
    SunCom          @tms.suncom.com
    T-mobile        @tmomail.net
    VoiceStream     @voicestream.net
    Verizon         @vtext.com

Finally,

    @a 0: p; program_path

would execute program_path at the starting time of the item.

The format for each of these:

    @a <trigger times> [: action [; arguments]]

In addition to the default action used when the optional : action is not given, there are the following possible values for action:

    d   Execute alert_displaycmd in etm.cfg.

    e; recipients[;attachments]     Send an email to recipients (a comma separated list of email addresses) optionally attaching attachments (a comma separated list of file paths). The item summary is used as the subject of the email and the expanded value of email_template from etm.cfg as the body.

    m   Display an internal etm message box using alert_template.

    p; process      Execute the command given by process.

    s   Execute alert_soundcmd in etm.cfg.

    t [; phonenumbers]      Send text messages to phonenumbers (a comma separated list of 10 digit phone numbers with the sms extension of the carrier appended) with the expanded value of sms.message as the text message.

    v   Execute alert_voicecmd in etm.cfg.

Note: either e or p can be combined with other actions in a single alert but not with one another.

@b beginby
----------

An integer number of days before the starting date time at which to begin displaying begin by notices. When notices are displayed they will be sorted by the item's starting datetime and then by the item's priority, if any.

@c context
----------

Intended primarily for tasks to indicate the context in which the task can be completed. Common contexts include home, office, phone, computer and errands. The "next view" supports this usage by showing undated tasks, grouped by context. If you're about to run errands, for example, you can open the "next view", look under "errands" and be sure that you will have no "wish I had remembered" regrets.

@d description
--------------

An elaboration of the details of the item to complement the summary.

@e extent
---------

A time period string such as 1d2h (1 day 2 hours). For an action, this would be the elapsed time. For a task, this could be an estimate of the time required for completion. For an event, this would be the duration. The ending time of the event would be this much later than the starting datetime.

Tip. Need to determine the appropriate value for @e for a flight when you have the departure and arrival datetimes but the timezones are different? The date calculator (shortcut F5) will accept timezone information so that, e.g., entering the arrival time minus the departure time

    4/20 6:15p US/Central - 4/20 4:50p Asia/Shanghai

into the calculator would give

    14h25m

as the flight time.

@f done[; due]
--------------

Datetimes; tasks, delegated tasks and task groups only. When a task is completed an @f done entry is added to the task. When the task has a due date, ; due is appended to the entry. Similarly, when a job from a task group is completed in etm, an &f done or &f done; due entry is appended to the job and it is removed from the list of prerequisites for the other jobs. In both cases done is the completion datetime and due, if added, is the datetime that the task or job was due. The completed task or job is shown as finished on the completion date. When the last job in a task group is finished an @f done or @f done; due entry is added to the task group itself reflecting the datetime that the last job was done and, if the task group is repeating, the &f entries are removed from the individual jobs.

Another step is taken for repeating task groups. When the first job in a task group is completed, the @s entry is updated using the setting for @o (above) to show the next datetime the task group is due and the @f entry is removed from the task group. This means when some, but not all of the jobs for the current repetition have been completed, only these job completions will be displayed. Otherwise, when none of the jobs for the current repetition have been completed, then only that last completion of the task group itself will be displayed.

Consider, for example, the following repeating task group which repeats monthly on the last weekday on or before the 25th.

    + pay bills @s 11/23 @f 10/24;10/25
      @r m &w MO,TU,WE,TH,FR &m 23,24,25 &s -1
      @j organize bills &q 1
      @j pay on-line bills &q 3
      @j get stamps, envelopes, checkbook &q 1
      @j write checks &q 2
      @j mail checks &q 3

Here "organize bills" and "get stamps, envelopes, checkbook" have no prerequisites. "Organize bills", however, is a prerequisite for "pay on-line bills" and both "organize bills" and "get stamps, envelops, checkbook" are prerequisites for "write checks" which, in turn, is a prerequisite for "mail checks".

The repetition that was due on 10/25 was completed on 10/24. The next repetition was due on 11/23 and, since none of the jobs for this repetition have been completed, the completion of the group on 10/24 and the list of jobs due on 11/23 will be displayed initially. The following sequence of screen shots show the effect of completing the jobs for the 11/23 repetition one by one on 11/27.

@g goto
-------

The path to a file or a URL to be opened using the system default application when the user presses G in the GUI. E.g., here's a task to join the etm discussion group with the URL of the group as the link. In this case, pressing G would open the URL in your default browser.

    - join the etm discussion group @s +1/1
      @g http://groups.google.com/group/eventandtaskmanager/topics

Tip. Have a pdf file with the agenda for a meeting? Stick an @g entry with the path to the file in the event you create for the meeting. Then whenever the meeting is selected, G will bring up the agenda.

@h history
----------

Used internally with task groups to track completion done;due pairs.

@j job
------

Component tasks or jobs within a task group are given by @j job entries. @key value entries prior to the first @j become the defaults for the jobs that follow. &key value entries given in jobs use & rather than @ and apply only to the specific job.

Many key-value pairs can be given either in the group task using @ or in the component jobs using &:

    @c or &c    context
    @d or &d    description
    @e or &e    extent
    @f or &f    done[; due] datetime
    @k or &k    keyword
    @l or &l    location
    @u or &u    user

The key-value pair &h is used internally to track job done;due completions in task groups.

The key-value pair &q (queue position) can only be given in component jobs where it is required. Key-values other than &q and those listed above, can only be given in the initial group task entry and their values are inherited by the component jobs.

@k keyword
----------

A heirarchical classifier for the item. Intended for actions to support time billing where a common format would be client:job:category. etm treats such a keyword as a heirarchy so that an action report grouped by month and then keyword might appear as follows

        27.5h) Client 1 (3)
            4.9h) Project A (1)
            15h) Project B (1)
            7.6h) Project C (1)
        24.2h) Client 2 (3)
            3.1h) Project D (1)
            21.1h) Project E (2)
                5.1h) Category a (1)
                16h) Category b (1)
        4.2h) Client 3 (1)
        8.7h) Client 4 (2)
            2.1h) Project F (1)
            6.6h) Project G (1)

An arbitrary number of heirarchical levels in keywords is supported.

@l location
-----------

The location at which, for example, an event will take place.

@m memo
-------

Further information about the item not included in the summary or the description. Since the summary is used as the subject of an email alert and the descripton is commonly included in the body of an email alert, this field could be used for information not to be included in the email.

@o overdue
----------

Repeating tasks only. One of the following choices: k) keep, r) restart, or s) skip. Details below.

@p priority
-----------

Either 0 (no priority) or an intger between 1 (highest priority) and 9 (lowest priority). Primarily used with undated tasks.

@r repetition rule
------------------

The specification of how an item is to repeat. Repeating items must have an @s entry as well as one or more @r entries. Generated datetimes are those satisfying any of the @r entries and falling on or after the datetime given in @s. Note that the datetime given in @s will only be included if it matches one of the datetimes generated by the @r entry.

A repetition rule begins with

    @r frequency

where frequency is one of the following characters:

    y       yearly
    m       monthly
    w       weekly
    d       daily
    h       hourly
    n       minutely
    l       list (a list of datetimes will be provided using @+)

The @r frequency entry can, optionally, be followed by one or more &key value pairs:

    &i: interval (positive integer, default = 1) E.g, with frequency w, interval 3 would repeat every three weeks.
    &t: total (positive integer) Include no more than this total number of repetitions.
    &s: bysetpos (integer). When multiple dates satisfy the rule, take the date from this position in the list, e.g, &s 1 would choose the first element and &s -1 the last. See the payday example below for an illustration of bysetpos.
    &u: until  (datetime) Only include repetitions falling **before** (not including) this datetime.
    &M: bymonth (1, 2, ..., 12)
    &m: bymonthday (1, 2, ..., 31) Use, e.g., -1 for the last day of the month.
    &W: byweekno (1, 2, ..., 53)
    &w: byweekday (*English* weekday abbreviation SU ... SA). Use, e.g., 3WE for the 3rd Wednesday or -1FR, for the last Friday in the month.
    &h: byhour (0 ... 23)
    &n: byminute (0 ... 59)

Repetition examples:

-   1st and 3rd Wednesdays of each month.

        ^ 1st and 3rd Wednesdays
          @r m &w 1WE, 3WE

-   Payday (an occasion) on the last week day of each month. (The &s -1 entry extracts the last date which is both a weekday and falls within the last three days of the month.)

        ^ payday @s 2010-07-01
          @r m &w MO, TU, WE, TH, FR &m -1, -2, -3 &s -1

-   Take a prescribed medication daily (an event) from the 23rd through the 27th of the current month at 10am, 2pm, 6pm and 10pm and trigger an alert zero minutes before each event.

        * take Rx @d 10a 23  @r d &u 11p 27 &h 10, 14 18, 22 @a 0

-   Vote for president (an occasion) every four years on the first Tuesday after a Monday in November. (The &m range(2,9) requires the month day to fall within 2 ... 8 and thus, combined with &w TU to be the first Tuesday following a Monday.)

        ^ Vote for president @s 2012-11-06
          @r y &i 4 &M 11 &m range(2,9) &w TU

Optionally, @+ and @- entries can be given.

-   @+: include (comma separated list to datetimes to be added to those generated by the @r entries)
-   @-: exclude (comma separated list to datetimes to be removed from those generated by the @r entries)

A repeating task may optionally also include an @o <k|s|r> entry (default = k):

-   @o k: Keep the current due date if it becomes overdue and use the next due date from the recurrence rule if it is finished early. This would be appropriate, for example, for the task 'file tax return'. The return due April 15, 2009 must still be filed even if it is overdue and the 2010 return won't be due until April 15, 2010 even if the 2009 return is finished early.

-   @o s: Skip overdue due dates and set the due date for the next repetition to the first due date from the recurrence rule on or after the current date. This would be appropriate, for example, for the task 'put out the trash' since there is no point in putting it out on Tuesday if it's picked up on Mondays. You might just as well wait until the next Monday to put it out. There's also no point in being reminded until the next Monday.

-   @o r: Restart the repetitions based on the last completion date. Suppose you want to mow the grass once every ten days and that when you mowed yesterday, you were already nine days past due. Then you want the next due date to be ten days from yesterday and not today. Similarly, if you were one day early when you mowed yesterday, then you would want the next due date to be ten days from yesterday and not ten days from today.

@s starting datetime
--------------------

When an action is started, an event begins or a task is due.

@t tags
-------

A tag or list of tags for the item.

@u user
-------

Intended to specify the person to whom a delegated task is assigned. Could also be used in actions to indicate the person performing the action.

@v action_rates key
-------------------

Actions only. A key from action_rates in your etm.cft to apply to the value of @e. Used in actions to apply a billing rate to time spent in an action. E.g., with

        minutes: 6
        action_rates:
            br1: 45.0
            br2: 60.0

then entries of @v br1 and @e 2h25m in an action would entail a value of 45.0 * 2.5 = 112.50.

@w action_markups key
---------------------

A key from action_markups in your etm.cfg to apply to the value of @x. Used in actions to apply a markup rate to expense in an action. E.g., with

        weights:
            mr1: 1.5
            mr2: 10.0

then entries of @w mr1 and @x 27.50 in an action would entail a value of 27.50 * 1.5 = 41.25.

@x expense
----------

Actions only. A currency amount such as 27.50. Used in conjunction with @w above to bill for action expenditures.

@z time zone
------------

The time zone of the item, e.g., US/Eastern. The starting and other datetimes in the item will be interpreted as belonging to this time zone.

Tip. You live in the US/Eastern time zone but a flight that departs Sydney on April 20 at 9pm bound for New York with a flight duration of 14 hours and 30 minutes. The hard way is to convert this to US/Eastern time and enter the flight using that time zone. The easy way is to use Australia/Sydney and skip the conversion:

    * Sydney to New York @s 2014-04-23 9pm @e 14h30m @z Australia/Sydney

This flight will be displayed while you're in the Australia/Sydney time zone as extending from 9pm on April 23 until 11:30am on April 24, but in the US/Eastern time zone it will be displayed as extending from 7am until 9:30pm on April 23.

@+ include
----------

A datetime or list of datetimes to be added to the repetitions generated by the @r rrule entry. If only a date is provided, 12:00am is assumed.

@- exclude
----------

A datetime or list of datetimes to be removed from the repetitions generated by the @r rrule entry. If only a date is provided, 12:00am is assumed.

Note that to exclude a datetime from the recurrence rule, the @- datetime must exactly match both the date and time generated by the recurrence rule.
"""

DATES = """\
-   Dates
    -   Fuzzy dates
    -   Time periods
    -   Time zones
    -   Anniversary substitutions

Dates
=====

Fuzzy dates
-----------

When either a datetime or an time period is to be entered, special formats are used in etm. Examples include entering a starting datetime for an item using @s, jumping to a date using Ctrl-J and calculating a date using F5.

Suppose, for example, that it is currently 8:30am on Friday, February 15, 2013. Then, fuzzy dates would expand into the values illustrated below.

        mon 2p or mon 14h    2:00pm Monday, February 19
        fri                  12:00am Friday, February 15
        9a -1/1 or 9h -1/1   9:00am Tuesday, January 1
        +2/15                12:00am Monday, April 15 2013
        8p +7 or 20h +7      8:00pm Friday, February 22
        -14                  12:00am Friday, February 1
        now                  8:30am Friday, February 15

Note that 12am is the default time when a time is not explicity entered. E.g., +2/15 in the examples above gives 12:00am on April 15.

To avoid ambiguity, always append either 'a', 'p' or 'h' when entering an hourly time, e.g., use 1p or 13h.

Time periods
------------

Time periods are entered using the format DdHhMm where D, H and M are integers and d, h and m refer to days, hours and minutes respectively. For example:

        2h30m                2 hours, 30 minutes
        7d                   7 days
        45m                  45 minutes

As an example, if it is currently 8:50am on Friday February 15, 2013, then entering now + 2d4h30m into the date calculator would give 2013-02-17 1:20pm.

Time zones
----------

Dates and times are always stored in etm data files as times in the time zone given by the entry for @z. On the other hand, dates and times are always displayed in etm using the local time zone of the system.

For example, if it is currently 8:50am EST on Friday February 15, 2013, and an item is saved on a system in the US/Eastern time zone containing the entry

    @s now @z Australia/Sydney

then the data file would contain

    @s 2013-02-16 12:50am @z Australia/Sydney

but this item would be displayed as starting at 8:50am 2013-02-15 on the system in the US/Eastern time zone.

Tip. Need to determine the flight time when the departing timezone is different that the arriving timezone? The date calculator (shortcut F5) will accept timezone information so that, e.g., entering the arrival time minus the departure time

    4/20 6:15p US/Central - 4/20 4:50p Asia/Shanghai

into the calculator would give

    14h25m

as the flight time.

Anniversary substitutions
-------------------------

An anniversary substitution is an expression of the form !YYYY! that appears in an item summary. Consider, for example, the occassion

    ^ !2010! anniversary @s 2011-02-20 @r y

This would appear on Feb 20 of 2011, 2012, 2013 and 2014, respectively, as 1st anniversary, 2nd anniversary, 3rd anniversary and 4th anniversary. The suffixes, st, nd and so forth, depend upon the translation file for the locale.
"""

PREFERENCES = """\
-   Preferences
    -   Template expansions
    -   Options

Preferences
===========

Configuration options are stored in a file named etmtk.cfg which, by default, belongs to the folder .etm in your home directory. When this file is edited in etm (Shift Ctrl-P), your changes become effective as soon as they are saved --- you do not need to restart etm. These options are listed below with illustrative entries and brief descriptions.

Template expansions
-------------------

The following template expansions can be used in alert_displaycmd, alert_template, alert_voicecmd, email_template, sms_message and sms_subject below.

!summary!

the item's summary (this will be used as the subject of email and message alerts)

!start_date!

the starting date of the event

!start_time!

the starting time of the event

!time_span!

the time span of the event (see below)

!alert_time!

the time the alert is triggered

!time_left!

the time remaining until the event starts

!when!

the time remaining until the event starts as a sentence (see below)

!d!

the item's @d (description)

!l!

the item's @l (location)

The value of !time_span! depends on the starting and ending datetimes. Here are some examples:

-   if the start and end datetimes are the same (zero extent): 10am Wed, Aug 4

-   else if the times are different but the dates are the same: 10am - 2pm Wed, Aug 4

-   else if the dates are different: 10am Wed, Aug 4 - 9am Thu, Aug 5

-   additionally, the year is appended if a date falls outside the current year:

        10am - 2pm Thu, Jan 3 2013
        10am Mon, Dec 31 - 2pm Thu, Jan 3 2013

Here are values of !time_left! and !when! for some illustrative periods:

-   2d3h15m

        time_left : '2 days 3 hours 15 minutes'
        when      : '2 days 3 hours 15 minutes from now'

-   20m

        time_left : '20 minutes'
        when      : '20 minutes from now'

-   0m

        time_left : ''
        when      : 'now'

Note that 'now', 'from now', 'days', 'day', 'hours' and so forth are determined by the translation file in use.

Options
-------

action_interval

    action_interval: 1

Every action_interval minutes, execute action_timercmd when the timer is running and action_pausecmd when the timer is paused. Choose zero to disable executing these commands.

action_markups

    action_markups:
        default: 1.0
        mu1: 1.5
        mu2: 2.0

Possible markup rates to use for @x expenses in actions. An arbitrary number of rates can be entered using whatever labels you like. These labels can then be used in actions in the @w field so that, e.g.,

    ... @x 25.80 @w mu1 ...

in an action would give this expansion in an action template:

    !expense! = 25.80
    !charge! = 38.70

action_minutes

    action_minutes: 6

Round action times up to the nearest action_minutes in action reports. Possible choices are 1, 6, 12, 15, 30 and 60. With 1, no rounding is done and times are reported as integer minutes. Otherwise, the prescribed rounding is done and times are reported as floating point hours.

action_rates

    action_rates:
        default: 30.0
        br1: 45.0
        br2: 60.0

Possible billing rates to use for @e times in actions. An arbitrary number of rates can be entered using whatever labels you like. These labels can then be used in the @v field in actions so that, e.g., with action_minutes: 6 then:

    ... @e 75m @v br1 ...

in an action would give these expansions in an action template:

    !hours! = 1.3
    !value! = 58.50

If the label default is used, the corresponding rate will be used when @v is not specified in an action.

Note that etm accumulates group totals from the time and value of individual actions. Thus

    ... @e 75m @v br1 ...
    ... @e 60m @v br2 ...

would aggregate to

    !hours!  = 2.3     (= 1.3 + 1)
    !value! = 118.50   (= 1.3 * 45.0 + 1 * 60.0)

action_template

    action_template: '!hours!h) !label! (!count!)'

Used for action reports. With the above settings for action_minutes and action_template, a report might appear as follows:

    27.5h) Client 1 (3)
        4.9h) Project A (1)
        15h) Project B (1)
        7.6h) Project C (1)
    24.2h) Client 2 (3)
        3.1h) Project D (1)
        21.1h) Project E (2)
            5.1h) Category a (1)
            16h) Category b (1)
    4.2h) Client 3 (1)
    8.7h) Client 4 (2)
        2.1h) Project F (1)
        6.6h) Project G (1)

Available template expansions for action_template include:

-   !label!: the item or group label.

-   !count!: the number of children represented in the reported item or group.

-   !minutes!: the total time from @e entries in minutes rounded up using the setting for action_minutes.

-   !hours!: if action_minutes = 1, the time in hours and minutes. Otherwise, the time in floating point hours.

-   !value!: the billing value of the rounded total time. Requires an action entry such as @v br1 and a setting for action_rates.

-   !expense!: the total expense from @x entries.

-   !charge!: the billing value of the total expense. Requires an action entry such as @w mu1 and a setting for action_markups.

-   !total!: the sum of !value! and !charge!.

Note: when aggregating amounts in action reports, billing and markup rates are applied first to times and expenses for individual actions and the resulting amounts are then aggregated. Similarly, when times are rounded up, the rounding is done for individual actions and the results are then aggregated.

action_timer

    action_timer:
        paused: 'play ~/.etm/sounds/timer_paused.wav'
        running: 'play ~/.etm/sounds/timer_running.wav'
        idle: 'play ~/.etm/sounds/timer_idle.wav'

The command running is executed every action_interval minutes whenever the action timer is running and paused every minute when the action timer is paused. The command idle is executed every action_interval minutes when the idle timer is running and the action timer is neither running nor paused.

agenda

    agenda_days: 4,
    agenda_colors: 2,
    agenda_indent: 2,
    agenda_width1: 43,
    agenda_width2: 17,

Sets the number of days with scheduled items to display in agenda view and other parameters affecting the display in the CLI.

alert_default

    alert_default: [m]

The alert or list of alerts to be used when an alert is specified for an item but the type is not given. Possible values for the list include: - d: display (requires alert_displaycmd) - m: message (using alert_template) - s: sound (requires alert_soundcmd) - v: voice (requires alert_voicecmd)

alert_displaycmd

    alert_displaycmd: growlnotify -t !summary! -m '!time_span!'

The command to be executed when d is included in an alert. Possible template expansions are discussed at the beginning of this tab.

alert_soundcmd

    alert_soundcmd: 'play ~/.etm/sounds/etm_alert.wav'

The command to execute when s is included in an alert. Possible template expansions are discussed at the beginning of this tab.

alert_template

    alert_template: '!time_span!\n!l!\n\n!d!'

The template to use for the body of m (message) alerts. See the discussion of template expansions at the beginning of this tab for other possible expansion items.

alert_voicecmd

    alert_voicecmd: say -v 'Alex' '!summary! begins !when!.'

The command to be executed when v is included in an alert. Possible expansions are are discussed at the beginning of this tab.

alert_wakecmd

    alert_wakecmd: ~/bin/SleepDisplay -w

If given, this command will be issued to "wake up the display" before executing alert_displaycmd.

ampm

    ampm: true

Use ampm times if true and twenty-four hour times if false. E.g., 2:30pm (true) or 14:30 (false).

completions_width

    completions_width: 36

The width in characters of the auto completions popup window.

calendars

    calendars:
    - [dag, true, personal/dag]
    - [erp, false, personal/erp]
    - [shared, true, shared]

These are (label, default, path relative to datadir) tuples to be interpreted as separate calendars. Those for which default is true will be displayed as default calendars. E.g., with the datadir below, dag would be a default calendar and would correspond to the absolute path /Users/dag/.etm/data/personal/dag. With this setting, the calendar selection dialog would appear as follows:

When non-default calendars are selected, busy times in the "week view" will appear in one color for events from default calendars and in another color for events from non-default calendars.

Only data files that belong to one of the calendar directories or their subdirectories will be accessible within etm.

cfg_files

    cfg_files:
        - completions: []
        - reports:     []
        - users:       []

Each of the three list brackets can contain one or more comma separated absolute file paths. Additionally, paths corresponding to active calendars in the datadir directory are searched for files named completions.cfg, reports.cfg and users.cfg and these are processed in addition to the ones from cfg_files.

Note. Windows users should place each absolute path in quotes and escape backslashes, i.e., use \\ anywhere \ appears in a path.

-   Completions

    Each line in a completions file provides a possible completion when using the editor. E.g. with these completions

        @c computer
        @c home
        @c errands
        @c office
        @c phone
        @z US/Eastern
        @z US/Central
        @z US/Mountain
        @z US/Pacific
        dnlgrhm@gmail.com

    entering, for example, "@c" in the editor and pressing Ctrl-Space, would popup a list of possible completions. Choosing the one you want and pressing Return would insert it and close the popup.

    Up and down arrow keys change the selection and either Tab or Return inserts the selection.

-   Reports

    Each line in a reports file provides a possible reports specification. These are available when using the CLI m command and in the GUI custom view. See Reports for details.

-   Users

    User files contain user (contact) information in a free form, text database. Each entry begins with a unique key for the person and is followed by detail lines each of which begins with a minus sign and contains some detail about the person that you want to record. Any detail line containing a colon should be quoted, e.g.,

        jbrown:
        - Brown, Joe
        - jbr@whatever.com
        - 'home: 123 456-7890'
        - 'birthday: 1978-12-14'
        dcharles:
        - Charles, Debbie
        - dch@sometime.com
        - 'cell: 456 789-0123'
        - 'spouse: Rebecca'

    Keys from this file are added to auto-completions so that if you type, say, @u jb and press Ctrl-Space, then @u jbrown would be offered for completion.

    If an item with the entry @u jbrown is selected in the GUI, you can press "u" to see a popup with the details:

        Brown, Joe
        jbr@whatever.com
        home: 123 456-7890
        birthday: 1978-12-14

current files

    current_htmlfile:  ''
    current_textfile:  ''
    current_indent:    3
    current_opts:      ''
    current_width1:    40
    current_width2:    17

If absolute file paths are entered for current_textfile and/or current_htmlfile, then these files will be created and automatically updated by etm as as plain text or html files, respectively. If current_opts is given then the file will contain a report using these options; otherwise the file will contain an agenda. Indent and widths are taken from these setting with other settings, including color, from report or agenda, respectively.

Hint: fans of geektool can use the shell command cat <current_textfile> to have the current agenda displayed on their desktops.

datadir

    datadir: ~/.etm/data

All etm data files are in this directory.

dayfirst

    dayfirst: false

If dayfirst is False, the MM-DD-YYYY format will have precedence over DD-MM-YYYY in an ambiguous date. See also yearfirst.

details_rows

    details_rows: 4

The number of rows to display in the bottom, details panel of the main window.

edit_cmd

    edit_cmd: ~/bin/vim !file! +!line!

This command is used in the command line version of etm to create and edit items. When the command is expanded, !file! will be replaced with the complete path of the file to be edited and !line! with the starting line number in the file. If the editor will open a new window, be sure to include the command to wait for the file to be closed before returning, e.g., with vim:

    edit_cmd: ~/bin/gvim -f !file! +!line!

or with sublime text:

    edit_cmd: ~/bin/subl -n -w !file!:!line!

email_template

    email_template: 'Time: !time_span!
    Locaton: !l!


    !d!'

Note that two newlines are required to get one empty line when the template is expanded. This template might expand as follows:

        Time: 1pm - 2:30pm Wed, Aug 4
        Location: Conference Room

        <contents of @d>

See the discussion of template expansions at the beginning of this tab for other possible expansion items.

etmdir

    etmdir: ~/.etm

Absolute path to the directory for etm.cfg and other etm configuration files.

encoding

    encoding: {file: utf-8, gui: utf-8, term: utf-8}

The encodings to be used for file IO, the GUI and terminal IO.

filechange_alert

    filechange_alert: 'play ~/.etm/sounds/etm_alert.wav'

The command to be executed when etm detects an external change in any of its data files. Leave this command empty to disable the notification.

fontsize_fixed

    fontsize_fixed: 0

Use this font size in the details panel, editor and reports. Use 0 to keep the system default.

fontsize_tree

    fontsize_tree: 0

Use this font size in the gui treeviews. Use 0 to keep the system default.

Tip: Leave the font sizes set to 0 and run etm with logging level 2 to see the system default sizes.

freetimes

    freetimes:
        opening:  480  # 8*60 minutes after midnight = 8am
        closing: 1020  # 17*60 minutes after midnight = 5pm
        minimum:   30  # 30 minutes
        buffer:    15  # 15 minutes

Only display free periods between opening and closing that last at least minimum minutes and preserve at least buffer minutes between events. Note that each of these settings must be an interger number of minutes.

E.g., with the above settings and these busy periods:

    Busy periods in Week 16: Apr 14 - 20, 2014
    ------------------------------------------
    Mon 14: 10:30am-11:00am; 12:00pm-1:00pm; 5:00pm-6:00pm
    Tue 15: 9:00am-10:00am
    Wed 16: 8:30am-9:30am; 2:00pm-3:00pm; 5:00pm-6:00pm
    Thu 17: 11:00am-12:00pm; 6:00pm-7:00pm; 7:00pm-9:00pm
    Fri 18: 3:00pm-4:00pm; 5:00pm-6:00pm
    Sat 19: 9:00am-10:30am; 7:30pm-10:00pm

This would be the corresponding list of free periods:

    Free periods in Week 16: Apr 14 - 20, 2014
    ------------------------------------------
    Mon 14: 8:00am-10:15am; 11:15am-11:45am; 1:15pm-4:45pm
    Tue 15: 8:00am-8:45am; 10:15am-5:00pm
    Wed 16: 9:45am-1:45pm; 3:15pm-4:45pm
    Thu 17: 8:00am-10:45am; 12:15pm-5:00pm
    Fri 18: 8:00am-2:45pm; 4:15pm-4:45pm
    Sat 19: 8:00am-8:45am; 10:45am-5:00pm
    Sun 20: 8:00am-5:00pm
    ----------------------------------------
    Only periods of at least 30 minutes are displayed.

When displaying free times in week view you will be prompted for the shortest period to display using the setting for minimum as the default.

Tip: Need to tell someone when you're free in a given week? Jump to that week in week view, press Ctrl-F, set the minimum period and then copy and paste the resulting list into an email.

iCalendar files

icscal_file

If an item is not selected, pressing Shift-X in the gui will export the active calendars in iCalendar format to this file.

    icscal_file: ~/.etm/etmcal.ics

icsitem_file

If an item is selected, pressing Shift-X in the gui will export the selected item in iCalendar format to this file.

    icsitem_file: ~/.etm/etmitem.ics

idle_minutes

    idle_minutes: 10

When the idle timer is running and an action timer is started or restarted, only open the dialog to assign idle time if the current idle time is at least this many minutes.

local_timezone

    local_timezone: US/Eastern

This timezone will be used as the default when a value for @z is not given in an item.

monthly

    monthly: monthly

Relative path from datadir. With the settings above and for datadir the suggested location for saving new items in, say, October 2012, would be the file:

    ~/.etm/data/monthly/2012/10.txt

The directories monthly and 2012 and the file 10.txt would, if necessary, be created. The user could either accept this default or choose a different file.

outline_depth

    outline_depth: 2

The default outline depth to use when opening keyword, note, path or tag view. Once any view is opened, use Ctrl-O to change the depth for that view.

prefix

    prefix: "\n  "
    prefix_uses: "rj+-tldm"

Apply prefix (whitespace only) to the @keys in prefix_uses when displaying and saving items. The default would cause the selected elements to begin on a newline and indented by two spaces. E.g.,

    + summary @s 2014-05-09 12am @z US/Eastern
      @m memo
      @j job 1 &f 20140510T1411;20140509T0000 &q 1
      @j job 2 &f 20140510T1412;20140509T0000 &q 2
      @j job 3 &q 3
      @d description

report

    report_begin:           '1'
    report_end:             '+1/1'
    report_colors:          2
    report_width1:          61
    report_width2:          19

Report begin and end are fuzzy parsed dates specifying the default period for reports that group by dates. Each line in the file specified by report_specifications provides a possible specification for a report. E.g.

    a MMM yyyy; k[0]; k[1:] -b -1/1 -e 1
    a k, MMM yyyy -b -1/1 -e 1
    c ddd MMM d yyyy
    c f

In custom view these appear in the report specifications pop-up list. A specification from the list can be selected and, perhaps, modified or an entirely new specification can be entered. See Reports for details. See also the agenda settings above.

show_finished

    show_finished: 1

Show this many of the most recent completions of repeated tasks or, if 0, show all completions.

smtp

    smtp_from: dnlgrhm@gmail.com
    smtp_id: dnlgrhm
    smtp_pw: **********
    smtp_server: smtp.gmail.com

Required settings for the smtp server to be used for email alerts.

sms

    sms_message: '!summary!'
    sms_subject: '!time_span!'
    sms_from: dnlgrhm@gmail.com
    sms_pw:  **********
    sms_phone: 0123456789@vtext.com
    sms_server: smtp.gmail.com:587

Required settings for text messaging in alerts. Enter the 10-digit area code and number and mms extension for the mobile phone to receive the text message when no numbers are specified in the alert. The illustrated phone number is for Verizon. Here are the mms extensions for the major carriers:

    Alltel          @message.alltel.com
    AT&T            @txt.att.net
    Nextel          @messaging.nextel.com
    Sprint          @messaging.sprintpcs.com
    SunCom          @tms.suncom.com
    T-mobile        @tmomail.net
    VoiceStream     @voicestream.net
    Verizon         @vtext.com

sundayfirst

    sundayfirst: false

The setting affects only the twelve month calendar display.

vcs_settings

    vcs_settings:
      command: ''
      commit: ''
      dir: ''
      file: ''
      history: ''
      init: ''
      limit: ''

These settings are ignored unless the setting for vcs_system below is either git or mercurial.

Default values will be provided for these settings based on the choice of vcs_system below. Any of the settings that you define here will overrule the defaults.

Here, for example, are the default values of these settings for git under OS X:

    vcs_settings:
        command: '/usr/bin/git --git-dir {repo} --work-dir {work}'
        commit: '/usr/bin/git --git-dir {repo} --work-dir {work} add */\*.txt
            && /usr/bin/git --git-dir {repo} --work-dir {work} commit -a -m "{mesg}"'
        dir: '.git'
        file: ''
        history: '/usr/bin/git -git-dir {repo} --work-dir {work} log
            --pretty=format:"- %ar: %an%n%w(70,0,4)%s" -U1  {numchanges}
                {file}'
        init: '/usr/bin/git init {work}; /usr/bin/git -git-dir {repo}
            --work-dir {work} add */\*.txt; /usr/bin/git-git-dir {repo}
                --work-dir {work} commit -a -m "{mesg}"'
        limit: '-n'

In these settings, {mesg} will be replaced with an internally generated commit message, {numchanges} with an expression that depends upon limit that determines how many changes to show and, when a file is selected, {file} with the corresponding path. If ~/.etm/data is your etm datadir, the {repo} would be replaced with ~/.etm/data/.git and {work} with ~/.etm/data.

Leave these settings empty to use the defaults.

vcs_system

    vcs_system: ''

This setting must be either '' or git or mercurial.

If you specify either git or mercurial here (and have it installed on your system), then etm will automatically commit any changes you make to any of your data files. The history of these changes is available in the GUI with the show changes command (Ctrl-H) and you can, of course, use any git or mercurial commands in your terminal to, for example, restore a previous version of a file.

weeks_after

    weeks_after: 52

In the day view, all non-repeating, dated items are shown. Additionally all repetitions of repeating items with a finite number of repetitions are shown. This includes 'list-only' repeating items and items with &u (until) or &t (total number of repetitions) entries. For repeating items with an infinite number of repetitions, those repetitions that occur within the first weeks_after weeks after the current week are displayed along with the first repetition after this interval. This assures that for infrequently repeating items such as voting for president, at least one repetition will be displayed.

yearfirst

    yearfirst: true

If yearfirst is true, the YY-MM-DD format will have precedence over MM-DD-YY in an ambiguous date. See also dayfirst.
"""

REPORTS = """\
-   Reports
    -   Report type characters
    -   Groupby setting
    -   Options

Reports
=======

To create a report open the custom view in the GUI. If you have entries in your report specifications file, ~./etm/reports.cfg by default, you can choose one of them in the selection box at the bottom of the window.

You can also add report specifications to the list by selecting any item from the list and then replacing the content with anything you like. Press Return to add your specification temporarily to the list. Note that the original entry will not be affected. When you leave the custom view you will have an opportunity to save the additions you have made. If you choose a file, your additions will be inserted into the list and it will be opened for editing.

When you have selected a report specification, press Return to generate the report and display it.

A report specification is created by entering a report type character, either "a" or "c", followed by a groupby setting and, perhaps, by one or more report options:

    <a|c> <groupby setting> [options]

Together, the type character, groupby setting and options determine which items will appear in the report and how they will be organized and displayed.

Report type characters
----------------------

-   a: action report.

    A report of expenditures of time and money recorded in actions with output formatted using action_template computations and expansions. See Preferences for further details about the role of action_template in formatting action report output.

-   c: composite report.

    Any item types, including actions, but without action_template computations and expansions. Note that only unfinished tasks and unfinished instances of repeating tasks will be displayed.

Groupby setting
---------------

A semicolon separated list that determines how items will be grouped and sorted. Possible elements include date specifications and elements from

-   c: context

-   f: file path

-   k: keyword

-   t: tag

-   u: user

A date specification is either

-   w: week number

or a combination of one or more of the following:

-   yy: 2-digit year

-   yyyy: 4-digit year

-   MM: month: 01 - 12

-   MMM: locale specific abbreviated month name: Jan - Dec

-   MMMM: locale specific month name: January - December

-   dd: month day: 01 - 31

-   ddd: locale specific abbreviated week day: Mon - Sun

-   dddd: locale specific week day: Monday - Sunday

For example, the report specification c ddd, MMM dd yyyy would group by year, month and day together to give output such as

    Fri, Apr 1 2011
        items for April 1
    Sat, Apr 2 2011
        items for April 2
    ...

On the other hand, the report specificaton a w; u; k[0]; k[1:] would group by week number, user and keywords to give output such as

    13.1) 2014 Week 14: Mar 31 - Apr 6
       6.3) agent 1
          1.3) client 1
             1.3) project 2
                1.3) Activity (12)
          5) client 2
             4.5) project 1
                4.5) Activity (21)
             0.5) project 2
                0.5) Activity (22)
       6.8) agent 2
          2.2) client 1
             2.2) project 2
                2.2) Activity (13)
          4.6) client 2
             3.9) project 1
                3.9) Activity (23)
             0.7) project 2
                0.7) Activity (23)

With the heirarchial elements, file path and keyword, it is possible to use parts of the element as well as the whole. Consider, for example, the file path A/B/C with the components [A, B, C]. Then for this file path:

    f[0] = A
    f[:2] = A/B
    f[2:] = C
    f = A/B/C

Suppose that keywords have the format client:project. Then grouping by year and month, then client and finally project to give output such as

    report: a MMM yyyy; u; k[0]; k[1] -b 1 -e +1/1

    13.1) Feb 2014
       6.3) agent 1
          1.3) client 1
             1.3) project 2
                1.3) Activity 12
          5) client 2
             4.5) project 1
                4.5) Activity 21
             0.5) project 2
                0.5) Activity 22
       6.8) agent 2
          2.2) client 1
             2.2) project 2
                2.2) Activity 13
          4.6) client 2
             3.9) project 1
                3.9) Activity 23
             0.7) project 2
                0.7) Activity 23

Items that are missing an element specified in groupby will be omitted from the output. E.g., undated tasks and notes will be omitted when a date specification is included, items without keywords will be omitted when k is included and so forth.

When a date specification is not included in the groupby setting, undated notes and tasks will be potentially included, but only those instances of dated items that correspond to the relevant datetime of the item of the item will be included, where the relevant datetime is the past due date for any past due tasks, the starting datetime for any non-repeating item and the datetime of the next instance for any repeating item.

Within groups, items are automatically sorted by date, type and time.

Options
-------

Report options are listed below. Report types c supports all options except -d. Report type a supports all options except -o and -h.

-b BEGIN_DATE

Fuzzy parsed date. Limit the display of dated items to those with datetimes falling on or after this datetime. Relative day and month expressions can also be used so that, for example, -b -14 would begin 14 days before the current date and -b -1/1 would begin on the first day of the previous month. It is also possible to add (or subtract) a time period from the fuzzy date, e.g., -b mon + 7d would begin with the second Monday falling on or after today. Default: None.

-c CONTEXT

Regular expression. Limit the display to items with contexts matching CONTEXT (ignoring case). Prepend an exclamation mark, i.e., use !CONTEXT rather than CONTEXT, to limit the display to items which do NOT have contexts matching CONTEXT.

-d DEPTH

CLI only. In the GUI use View/Set outline depth. The default, -d 0, includes all outline levels. Use -d 1 to include only level 1, -d 2 to include levels 1 and 2 and so forth. This setting applies to the CLI only. In the GUI use the command set outline depth.

For example, modifying the report above by adding -d 3 would give the following:

    report: a MMM yyyy; u; k[0]; k[1] -b 1 -e +1/1 -d 3

    13.1) Feb 2014
       6.3) agent 1
          1.3) client 1
          5) client 2
       6.8) agent 2
          2.2) client 1
          4.6) client 2

-e END_DATE

Fuzzy parsed date. Limit the display of dated items to those with datetimes falling before this datetime. As with BEGIN_DATE relative month expressions can be used so that, for example, -b -1/1  -e 1 would include all items from the previous month. As with -b, period strings can be appended, e.g., -b mon -e mon + 7d would include items from the week that begins with the first Monday falling on or after today. Default: None.

-f FILE

Regular expression. Limit the display to items from files whose paths match FILE (ignoring case). Prepend an exclamation mark, i.e., use !FILE rather than FILE, to limit the display to items from files whose path does NOT match FILE.

-k KEYWORD

Regular expression. Limit the display to items with contexts matching KEYWORD (ignoring case). Prepend an exclamation mark, i.e., use !KEYWORD rather than KEYWORD, to limit the display to items which do NOT have keywords matching KEYWORD.

-l LOCATION

Regular expression. Limit the display to items with location matching LOCATION (ignoring case). Prepend an exclamation mark, i.e., use !LOCATION rather than LOCATION, to limit the display to items which do NOT have a location that matches LOCATION.

-o OMIT

String. Composite reports only. Show/hide a)ctions, d)elegated tasks, e)vents, g)roup tasks, n)otes, o)ccasions and/or other t)asks. For example, -o on would show everything except occasions and notes and -o !on would show only occasions and notes.

-s SUMMARY

Regular expression. Limit the display to items containing SUMMARY (ignoring case) in the item summary. Prepend an exclamation mark, i.e., use !SUMMARY rather than SUMMARY, to limit the display to items which do NOT contain SUMMARY in the summary.

-S SEARCH

Regular expression. Composite reports only. Limit the display to items containing SEARCH (ignoring case) anywhere in the item or its file path. Prepend an exclamation mark, i.e., use !SEARCH rather than SEARCH, to limit the display to items which do NOT contain SEARCH in the item or its file path.

-t TAGS

Comma separated list of case insensitive regular expressions. E.g., use

    -t tag1, !tag2

or

    -t tag1, -t !tag2

to display items with one or more tags that match 'tag1' but none that match 'tag2'.

-u USER

Regular expression. Limit the display to items with user matching USER (ignoring case). Prepend an exclamation mark, i.e., use !USER rather than USER, to limit the display to items which do NOT have a user that matches USER.
"""

