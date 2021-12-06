# REQUIREMENTS

*DRAFT*

This is an evolving document for requirements of the Agenda Tool,
from audience requirements, to functional requirements, and
Infrastructure (maintenance) requirements.

*DRAFT*

## Audience Requirements

There are multiple audiences for the tool.

* Directors of the Board
* Vice Presidents of the Project Management Committees
* Interested Members of the Foundation
* Guests invited to a Board meeting


## Functional Requirements

Raw list of features that are in-use today.
*Refinement needed*

* Generate new agenda from a template
  * Given current set of Directors and Officers
  * Based on which PMCs are due to report for "this" month
* Post a PMC report
* Directors can review, sign-off, comment, and flag reports
* Provide active workflow during a Board meeting
  * Special functions for: Chairman, Directors, Secretary, Members/Guests
  * Display "flagged" projects
* Track action items (finer points of this: TBD)
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
