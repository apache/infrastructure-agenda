# REQUIREMENTS

*DRAFT*

This is an evolving document for requirements of the Agenda Tool,
from audience requirements, to functional requirements, and
Infrastructure (maintenance) requirements.

*DRAFT*

## Audience Requirements

There are multiple audiences for the tool.

* Directors of the Board
* Chair of the Board
* Secretary
* Vice Presidents of the Project Management Committees
* Interested Members of the Foundation
* Guests invited to a Board meeting

## Functional Requirements

Raw list of features that are in-use today.
*Refinement needed*

* Generate new agenda from a template _(Secretary, Chair)_
  * Given current set of Directors, Officers, and Guests
  * Based on which PMCs are due to report for "this" month
    * Based on published schedule
    * Based on flagged to report since last meeting 
  * Carry over unfinished items (Actions, Discussions, Unfinished Business, other?) from last month
  * Automatically assign shepherds
* Post or edit a PMC report _(PMC VPs, Members)_
 * Tool integration with Reporter 
* Post or edit Resolutions based on templates
 * Tool integration with Incubator, Attic, etc.; with PODLINGNAMESEARCH; with LDAP
 * _(TBD)_ Workflow integrations with resolutions:
  * New Project: push data to Infra (new TLP; new committers/PMC; new VP) and Incubator
  * Attic Project: push data to Infra and Attic (TLP/committers/PMC delete; VP delete)
  * Change PMC VP: send new officer/thanks old officer email in post-meeting publish
  * Appoint officer: send new officer welcome email in post-meeting publish
* Directors can review, sign-off, comment, and flag reports
  * PMC VPs can read and comment on reports
  * Comments can be targetted at the PMC, which includes notifications to the PMC
  * Comments can be targetted at the board, without notifications to the PMC.
  * Any agenda item from Minutes through Special Orders can be commented on.
* Provide active workflow during a Board meeting
  * Special functions for: Chair, Directors, Secretary, Members/Guests
    * Chair features:
      * Mark current position in agenda being discussed, so other users can follow the agenda during meeting
      * Can use next/back buttons to easily progress through meeting in defined order (i.e. flagged reports, etc.) 
    * Secretary features:
      * Open and close meeting with timestamps
      * Record votes or decisions on items
      * Record comments on items
      * Record Action Items associated with an item assigned to an individual
    * Directors can review, sign-off, comment, and flag reports during meeting
  * Display only "flagged" projects or reports (including officers) in order
  * Display only "unapproved" project reports in order
* Track action items (finer points of this: TBD)
* Archive private version of agenda before monthly meeting
* Post-Meeting publishing:
  * Publish **public** version of meeting minutes after meeting
  * Execute workflow on any Resolutions **passed**
  * Prepare committers@ Board meeting recap email (projects and their VP's added/deleted; new officers appointed)
* single button attend/regret
* show local time in call to order
* show draft minutes
* queue of pending reports
* hotlink urls, JIRA, CVE
* enbolden asf members in resolutions
* visual indication of whether a report is flagged, needs more approvals, has sufficient preapprovals, etc
* reflow reports
* should show related information - e.g., action items, special orders, and history of missing reports, history of previous board comments, prior reports, roster, etc. associated with current report
* for missing reports, it should indicate if a report has been posted to board@ during the past month, and assist with the posting of the report
* send reminders
  * template based on missing status the previous month(s)
  * first and final reminder selection should include all missing project reports by default, including non-responsive PMCs
* draft emails for late reports
* show shepard reports - with easy navigation to only reports you are sheparding
* search function
* show a global list of comments - with ability to mark as seen
* offline support
* should only require a single authentication step for all functionality
* *more TBD*

## Infrastructure Requirements

* Server code must be written in Python
  * Note: a prototype server has been started using JavaScript. An argument
    can be made that restarting development of the server in Python may be
    reasonable, relative to the work to complete the JavaScript prototype
    (when consider skillsets and long-term maintenance)
  * The existing Agenda Tool is written in Ruby, which cannot be maintained
    by the Infrastructure Team. There are no plans to add Ruby skills to
    the team.
* Technologies that are (generally) within the existing set (eg. cloud
  services, backups, configuration management (such as Puppet), and other
  tech that is within typical scope)


# Data Structures And Workflows

While much of the monthly agenda is boilerplate text with lists of data 
plugged in (like names in Call To Order), some items in the agenda have 
data structures or workflows used elsewhere in the ASF.  In particular, 
Secretary, Infra, Incubator, Attic, and general LDAP records need various
update data provided after the meeting for some workflows. 

Also note that agenda items should have all state archived privately, and 
select data and indicies must be archived publicly (by date; by 
project/officer, etc.)

## General Data Requirements

The resulting data, once a Board meeting is over, must be available in an open structured format, such as JSON or structured text, to allow for:

  * Long-term structured archiving of the Board's decisions and comments
  * Enabling other tools to generate specific views of the results, like [listing all reports of a given project](https://whimsy.apache.org/board/minutes/Ant).

Access to other ASF data (usually read-only, such as [committee-info.txt](https://svn.apache.org/repos/private/committers/board/committee-info.txt)) might go through a specific subdomain like data.apache.org (or two: one private, one public) to help keep track, over time, of what data is used and to clarify access control.

## All Items
- Item ID (where in Agenda)
- Title (boilerplate style or free form)
- Submitter (new: we should really track who submitted each item)

## Report

- Title (PMC name or Officer's name)
- Author (PMC VP or Officer)
- Shepherd (Director)
- Text (markdown document of contents)
- Status (approvals; flagged (by who); comments)

### Report Workflow

- **Pre-Meeting Workflow**
  - Secretary, Chair: Add specific Report and assign ItemNum (agenda create; ItemNum should remain stable)
  - PMC VPs, Officer: Add their own Report (out-of-band: default an ItemNum value)
  - Member: Edit any report
  - Director: Preapprove; Flag; Comment (add new to list, or edit own)
- **During Meeting Workflow**
  - Secretary, Chair: edit any report (but not other roles)
  - Director: Preapprove; Flag; Comment (add new to list, or edit own)
- **Post Meeting Workflow**
  - Secretary: mark EndStatus: Accepted, Missing, Rejected
  - List reports Missing/Rejected (for summary email)
  - List reports expected next month (for summary; for next agenda)
- **Public Archive Workflow**
  - Do not publish: 
    - _private_ sections
    - Approvals, Flags, Comments

## Resolution

- Title - boilerplate for new TLP, Attic, Chair Change; otherwise free text
- Submitter (PMC VP or Officer)
- Text (boilerplate contents or free form)
- Status (comments; board vote status or general consent)

### Resolution Workflow

- **Pre-Meeting Workflow**
  - Member: Add resolution
  - Director: Preapprove / pre-vote; Comment (add new to list, or edit own); Three levels of report selection are useful:
     -  Start with "reports where I'm shepherd", currently possible by searching for Director's name on the Agenda page and opening those reports in a new browser tab for review.
     -  Then, select "reports which don't have enough pre-approvals" using the Navigation/Queue list, next/previous buttons navigate in this list or open those reports (based on their colors in the list) in a new tab as in the previous phase.
     -  And lastly look at the Navigation/Queue for reports that haven't been reviewed by this Director yet
- **During Meeting Workflow**
  - Secretary, Chair: edit any resolution (but not other roles)
  - Secretary: record director votes or table/postpone
- **Post Meeting Workflow**
  - List resolutions and status (for summary email)
  - Carry-over tabled resolutions to next agenda
- **Public Archive Workflow**
  - Do not publish: 
    - _private_ sections
    - Comments

## New TLP Resolution

As Resolution plus:

- TLP Boilerplate
- Incubator Graduate or Straight-To-TLP?
- PMC name
- PMC purpose (creation of software to manage widgets...)
- PMC VP
- PMC Members (list)
  - Display VP;Members as Public Name, ID, with bold for ASF Members

- **Post Meeting Workflow**
  - Inform Infra of new TLP Name, list of PMC members & VP
    - Various LDAP and other updates
  - Inform Incubator (if is a graduation)
  - Inform press@ of new project

## Attic TLP Resolution

As Resolution plus:

- Attic Boilerplate
- PMC name
- PMC VP
- Link/commentary to attic vote (?)

- **Post Meeting Workflow**
  - Inform Infra of TLP Name, VP, list of members
    - Various LDAP Updates (?)
  - Inform Attic
  - Inform press@ of terminated project

## Chair Change Resolution

As Resolution plus:

- Chair Change Boilerplate
- PMC name
- PMC VP name - outgoing 
- PMC VP name - incoming 

- **Post Meeting Workflow**
  - Inform Infra of new VP for LDAP update
  - Inform new VP, outgoing VP of role change
  - Inform PMC of the role change (? We don't do this now, but should)

## Discussion Item

- Text
- (?) Should we add Comments list to discussion items too?
- (?) Should we add Status to discussion items too?
- TBD: definition if items are carried over to next agenda?

## Action Item

- Text
- Owner
- Linked Report (PMC, officer, etc)(optional)
- Status

### Action Item Workflows

- Secretary can create on the fly during meeting, link by default to current discussion item
- Members can update data at any point
- Chair/Secretary decide post-meeting which AIs to carry over to next agenda
- TBD: post-meeting Secretary email should inform Owner of new AIs
