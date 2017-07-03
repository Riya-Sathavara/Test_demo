Open ERP System :- Odoo 10 Community

Installation 
============
Install the Application => Apps -> Saudi GR(Technical Name:saudi_gr)

Module Configration Guideline
=============================
	1. Old Users give rights of 'GR User' for access and create GR related operation:
	   Settings -> Users -> Gr Operation -> User

	2. New Users have default rights Gr Operation User to access Gr Operation:

	3. Add Required Document list for all GR operations so every timje you don't need to write while create any operation.
	   Employee -> Configuration (KSA) -> Gr Operations -> GR Required Document

	4. Add list of Religion:
	   Employee -> Configuration (KSA) -> Gr Operations -> Religion

	5. Add Other GR Operation:
	   Employee -> Configuration (KSA) -> Gr Operations -> GR Operation':
Employee
========
	
	1. Create Employee for each user.
	   Employee -> Create
	   Set "related User" in HR Setting Tab.
	   Add employee related details.
	   Add date of joining, Arabic name, gosi number if employee have in "GR operation" tab.


Roles
=====
Basically GR operations have two Roles
1. User
2. Manager 

1. Visa Request
   USER:
	1. User have access create only their "Visa Request"
	2. When you enter Visa Duration it will automatic calculate Approved Date To in Visa request.
	3. User only able to view required document list in "required document" tab.
	4. User can only able to confirm and cancel their visa request.
	5. User can only view who is validated or Approved their 'visa request' in last "Extra Information.

   MANAGER:
	1. Manager have access create, view and delete "Visa Request" for any employee.
	2. When manager enter Visa Duration it will automatic calculate Approved Date To in Visa request.
	3. Manager can able to edit required document list in "required document" tab.
	4. Manager can able to validate and Approve visa request.
	5. Manager can able to refuse any visa application.

2. Visa Iqama
   USER:
	1. User have access create only their "Iqama"
	2. User only able to view required document list in "required document" tab.
	3. User can only able to confirm their and cancel Iqama request.
	4. User can only view who is validated or Approved their 'Iqama request' in last "Extra Information.

   MANAGER:
	1. Manager have access create, view and delete "Iqama Request" for any employee.
	3. Manager can able to edit required document list in "required document" tab.
	4. Manager can able to validate and Approve visa request.
	5. Manager can able to refuse any visa application.


3. Sponsorship Transfer
   USER:
	1. User have access create only their "Sponsorship Transfer"
	2. User only able to view required document list in "required document" tab.
	3. User can only able to confirm their and cancel Sponsorship Transfer request.
	4. User can only view who is validated or Approved their 'Sponsorship Transfer request' in last "Extra Information.

   MANAGER:
	1. Manager have access create, view and delete "Sponsorship Transfer Request" for any employee.
	3. Manager can able to edit required document list in "required document" tab.
	4. Manager can able to validate and Approve Sponsorship Transfer request.
	5. Manager can able to refuse any Sponsorship Transfer application.



