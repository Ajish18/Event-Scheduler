This is a Flask + SQLite based application that helps manage events, resources, allocations, and generates availability & usage reports.

It includes:
      Event CRUD,
      Resource CRUD,
      Allocation with conflict checking,
      Report generation between selected dates,
      Simple and clean UI

Tech Stack
      Python (Flask),
      SQLite,
      HTML, CSS (Jinja Templates)

Working of the App:
Run the app and open the Home page. From there, click on “Schedule Events.
<img width="1913" height="945" alt="image" src="https://github.com/user-attachments/assets/2f5b4b9f-b16e-460a-875d-4e9b3127c919" />

You will enter the Events page, where you can see the list of all events.
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/de1ab723-73a4-438f-ac11-e5b66d8a9be4" />

To add new resources or view/edit existing ones, click “Manage Resources.”
<img width="1919" height="1012" alt="image" src="https://github.com/user-attachments/assets/1ef05a2b-e631-47a7-be99-27157f82e2bf" />

In the Resources page, click “Add Resource,” fill in the resource name, select the resource type, and then click Save.
<img width="1919" height="951" alt="image" src="https://github.com/user-attachments/assets/b8c9fab5-4efb-4f74-817d-d900089593cc" />
You will be taken to the Resources page, where you can see the newly added resource along with existing ones. Click “Edit” on any resource you want to modify.
<img width="1919" height="998" alt="image" src="https://github.com/user-attachments/assets/62878501-a1ed-4163-87cc-b02158406f8f" />
Click “Edit” to update the resource and then click Save. Click “Delete” to remove the resource, and confirm the action by clicking OK in the pop-up.
<img width="1919" height="1002" alt="image" src="https://github.com/user-attachments/assets/41eababa-792a-4b16-b451-42a6e85b3692" />

Go back to event page and click Add new events.
<img width="1918" height="1013" alt="image" src="https://github.com/user-attachments/assets/55b99545-ea4f-4b70-a8e7-759be2661797" />

Enter the title, start time, end time and description and click save.
<img width="1918" height="1013" alt="image" src="https://github.com/user-attachments/assets/d9afbd5a-5911-41cc-bde4-30479b6ec39a" />
<img width="1919" height="1007" alt="image" src="https://github.com/user-attachments/assets/f81e0543-a487-435b-9ef9-f5a818cc02eb" />
You will be redirected to the Events Page. You can see the newly added event.
<img width="1919" height="1002" alt="image" src="https://github.com/user-attachments/assets/f94a6632-af38-402a-bf1e-eaa236288534" />

Click “Edit” on the event you want to modify.
<img width="1919" height="998" alt="image" src="https://github.com/user-attachments/assets/d02ab5ab-596e-4dc9-8dab-a8d96eb02a0d" />
Modify the details and click save.
<img width="1919" height="998" alt="image" src="https://github.com/user-attachments/assets/a5dbae77-ebb1-4817-8616-ab39e77b56f8" />
Click “Allocate” to assign available resources to that event without any conflicts.
<img width="1919" height="1003" alt="image" src="https://github.com/user-attachments/assets/304031ec-3c65-4b85-9fab-e5cf165a9f42" />
Allocate the resources and click Save. You will be redirected to the Events page. To verify whether the resources were allocated, click “Allocate” for that event again.
<img width="1919" height="1004" alt="image" src="https://github.com/user-attachments/assets/d2272dbf-0100-4ea0-bb1b-77bedc18b2fa" />
Click Delete to delete the event.
<img width="1891" height="992" alt="image" src="https://github.com/user-attachments/assets/b8571452-9594-4243-9fcd-4f503910289e" />

Click "View Report" to generate Report.
<img width="1919" height="1007" alt="image" src="https://github.com/user-attachments/assets/bd57e675-5b33-40ef-b4d8-a21bf3ee9a21" />

Select the Date and click Generate Report. Your Report will be Generated.
<img width="1919" height="999" alt="image" src="https://github.com/user-attachments/assets/8e46d4ad-c052-4349-aa68-aed012190509" />

Video Link - https://drive.google.com/file/d/1Nuy0dVrxrQZt-p2Y59dZ9GpDuGTd8piA/view?usp=sharing

Thanking you
