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
  * Carry over unfinished items (Actions, Discussions, other?) from last month
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
