import json
import datetime


body = b'{"event":"job.updated","company_id":"d3514589-8266-4fcf-aa56-af658b20f8ab","job":{"id":"job_360dde95efb04ce29ccd8de2558b4410","invoice_number":"21","description":"Mobile Carwash \\u0026 Detailing","customer":{"id":"cus_816acd9103d2483d8f5afdee8e9981b0","first_name":"Aleksandr","last_name":"El","email":"elin.alexander88@gmail.com","mobile_number":"3126848315","home_number":null,"work_number":null,"company":null,"notifications_enabled":true,"lead_source":null,"notes":null,"created_at":"2024-08-18T18:11:06Z","updated_at":"2024-08-18T18:11:06Z","company_name":"VAST CLEANING","company_id":"d3514589-8266-4fcf-aa56-af658b20f8ab","tags":[]},"address":{"id":"adr_29c19df094384c8d87b4683bba262911","type":"service","street":"12 E 8th St","street_line_2":"1803","city":"Chicago","state":"IL","zip":"60605","country":"US"},"notes":[{"id":"nte_4d608f336aaf418eab40596796b0f01d","content":"kjjk\\n"}],"work_status":"in progress","work_timestamps":{"on_my_way_at":"2024-08-26T16:36:39Z","started_at":null,"completed_at":null},"schedule":{"scheduled_start":"2024-08-28T17:00:00Z","scheduled_end":"2024-08-28T18:00:00Z","arrival_window":0,"appointments":[]},"total_amount":108100,"outstanding_balance":108100,"assigned_employees":[{"id":"pro_d732eca4f2804f588828b9b5522973ab","first_name":"Arkadii","last_name":"Astvatsaturov","email":"arkady017@gmail.com","mobile_number":"7639103848","color_hex":"EF9159","avatar_url":"/assets/add_image_thumb.png","role":"field tech","tags":[],"permissions":{"can_add_and_edit_job":true,"can_be_booked_online":true,"can_call_and_text_with_customers":true,"can_chat_with_customers":true,"can_delete_and_cancel_job":true,"can_edit_message_on_invoice":true,"can_see_street_view_data":true,"can_share_job":false,"can_take_payment_see_prices":true,"can_see_customers":true,"can_see_full_schedule":true,"can_see_future_jobs":true,"can_see_marketing_campaigns":true,"can_see_reporting":true,"can_edit_settings":true,"is_point_of_contact":false,"is_admin":true},"company_name":"VAST CLEANING","company_id":"d3514589-8266-4fcf-aa56-af658b20f8ab"}],"tags":[],"original_estimate_id":null,"original_estimate_uuids":[],"lead_source":null,"job_fields":{"job_type":{"id":"jbt_deea0746ba044e1ab08abd787b8f8139","name":"One-time clean"},"business_unit":null},"created_at":"2024-08-26T16:19:35Z","updated_at":"2024-08-26T16:38:42Z","company_name":"VAST CLEANING","company_id":"d3514589-8266-4fcf-aa56-af658b20f8ab","attachments":[]}}'


'{"event":"customer.created","company_id":"d3514589-8266-4fcf-aa56-af658b20f8ab","customer":{"id":"cus_bfec81a415e14f499806079024e528bd","first_name":"Kathleen","last_name":"Gandara","email":"photokathy@yahoo.com","mobile_number":"6262982737","home_number":null,"work_number":null,"company":null,"notifications_enabled":true,"lead_source":null,"notes":null,"created_at":"2024-08-28T20:35:29Z","updated_at":"2024-08-28T20:35:29Z","company_name":"VAST CLEANING","company_id":"d3514589-8266-4fcf-aa56-af658b20f8ab","tags":[],"addresses":[{"id":"adr_2489d8fe3ca1416fa34952fcb4ec0dcd","type":"service","street":"711 Orange Grove Avenue","street_line_2":"","city":"South Pasadena","state":"CA","zip":"91030","country":"US"}],"attachments":[]}}'
'{"event":"job.created","company_id":"d3514589-8266-4fcf-aa56-af658b20f8ab","job":{"id":"job_0f9a7aa91bde46259cd6365db87c4ebf","invoice_number":"22","description":"Apartments Cleaning","customer":{"id":"cus_bfec81a415e14f499806079024e528bd","first_name":"Kathleen","last_name":"Gandara","email":"photokathy@yahoo.com","mobile_number":"6262982737","home_number":null,"work_number":null,"company":null,"notifications_enabled":true,"lead_source":null,"notes":null,"created_at":"2024-08-28T20:35:29Z","updated_at":"2024-08-28T20:35:29Z","company_name":"VAST CLEANING","company_id":"d3514589-8266-4fcf-aa56-af658b20f8ab","tags":[]},"address":{"id":"adr_2489d8fe3ca1416fa34952fcb4ec0dcd","type":"service","street":"711 Orange Grove Avenue","street_line_2":"","city":"South Pasadena","state":"CA","zip":"91030","country":"US"},"notes":[{"id":"nte_932a8fc3a351425fb0028d1e557058de","content":"Apartments Cleaning:\\nDescription:\\n- Kitchen and bathroom only"}],"work_status":"scheduled","work_timestamps":{"on_my_way_at":null,"started_at":null,"completed_at":null},"schedule":{"scheduled_start":"2024-08-30T17:00:00Z","scheduled_end":"2024-08-30T17:00:00Z","arrival_window":0,"appointments":[]},"total_amount":14900,"outstanding_balance":14900,"assigned_employees":[{"id":"pro_d732eca4f2804f588828b9b5522973ab","first_name":"Arkadii","last_name":"Astvatsaturov","email":"arkady017@gmail.com","mobile_number":"7639103848","color_hex":"EF9159","avatar_url":"/assets/add_image_thumb.png","role":"field tech","tags":[],"permissions":{"can_add_and_edit_job":true,"can_be_booked_online":true,"can_call_and_text_with_customers":true,"can_chat_with_customers":true,"can_delete_and_cancel_job":true,"can_edit_message_on_invoice":true,"can_see_street_view_data":true,"can_share_job":false,"can_take_payment_see_prices":true,"can_see_customers":true,"can_see_full_schedule":true,"can_see_future_jobs":true,"can_see_marketing_campaigns":true,"can_see_reporting":true,"can_edit_settings":true,"is_point_of_contact":false,"is_admin":true},"company_name":"VAST CLEANING","company_id":"d3514589-8266-4fcf-aa56-af658b20f8ab"}],"tags":[],"original_estimate_id":null,"original_estimate_uuids":[],"lead_source":"Online Booking","job_fields":{"job_type":null,"business_unit":null},"created_at":"2024-08-28T20:35:29Z","updated_at":"2024-08-28T20:35:30Z","company_name":"VAST CLEANING","company_id":"d3514589-8266-4fcf-aa56-af658b20f8ab","attachments":[]}}'
'{"event":"job.updated","company_id":"d3514589-8266-4fcf-aa56-af658b20f8ab","job":{"id":"job_360dde95efb04ce29ccd8de2558b4410","invoice_number":"21","description":"Mobile Carwash \\u0026 Detailing","customer":{"id":"cus_816acd9103d2483d8f5afdee8e9981b0","first_name":"Aleksandr","last_name":"El","email":"elin.alexander88@gmail.com","mobile_number":"3126848315","home_number":null,"work_number":null,"company":null,"notifications_enabled":true,"lead_source":null,"notes":null,"created_at":"2024-08-18T18:11:06Z","updated_at":"2024-08-18T18:11:06Z","company_name":"VAST CLEANING","company_id":"d3514589-8266-4fcf-aa56-af658b20f8ab","tags":[]},"address":{"id":"adr_29c19df094384c8d87b4683bba262911","type":"service","street":"12 E 8th St","street_line_2":"1803","city":"Chicago","state":"IL","zip":"60605","country":"US"},"notes":[{"id":"nte_4d608f336aaf418eab40596796b0f01d","content":"kjjk\\n"}],"work_status":"in progress","work_timestamps":{"on_my_way_at":"2024-08-26T16:36:39Z","started_at":null,"completed_at":null},"schedule":{"scheduled_start":"2024-08-28T17:00:00Z","scheduled_end":"2024-08-28T18:00:00Z","arrival_window":0,"appointments":[]},"total_amount":108100,"outstanding_balance":108100,"assigned_employees":[{"id":"pro_d732eca4f2804f588828b9b5522973ab","first_name":"Arkadii","last_name":"Astvatsaturov","email":"arkady017@gmail.com","mobile_number":"7639103848","color_hex":"EF9159","avatar_url":"/assets/add_image_thumb.png","role":"field tech","tags":[],"permissions":{"can_add_and_edit_job":true,"can_be_booked_online":true,"can_call_and_text_with_customers":true,"can_chat_with_customers":true,"can_delete_and_cancel_job":true,"can_edit_message_on_invoice":true,"can_see_street_view_data":true,"can_share_job":false,"can_take_payment_see_prices":true,"can_see_customers":true,"can_see_full_schedule":true,"can_see_future_jobs":true,"can_see_marketing_campaigns":true,"can_see_reporting":true,"can_edit_settings":true,"is_point_of_contact":false,"is_admin":true},"company_name":"VAST CLEANING","company_id":"d3514589-8266-4fcf-aa56-af658b20f8ab"}],"tags":[],"original_estimate_id":null,"original_estimate_uuids":[],"lead_source":null,"job_fields":{"job_type":{"id":"jbt_deea0746ba044e1ab08abd787b8f8139","name":"One-time clean"},"business_unit":null},"created_at":"2024-08-26T16:19:35Z","updated_at":"2024-08-26T16:38:42Z","company_name":"VAST CLEANING","company_id":"d3514589-8266-4fcf-aa56-af658b20f8ab","attachments":[]}}'


data = json.loads(body.decode())
print(data)

d_str = "2024-08-28T17:00:00Z"
format = "%Y-%m-%dT%H:%M:%S%z"

print(datetime.datetime.strptime(d_str, format))

s1 = "s1"
s2 = ""
s3 = "s3"
print(s1 + s2 + s3)
from enum import Enum


class JobStatus(str, Enum):
    unscheduled: str = "needs scheduling"
    scheduled: str = "scheduled"
    in_progress: str = "in progress"  # job.started
    completed: str = "complete unrated"  # job.completed
    canceled: str = "pro canceled"

b = JobStatus.scheduled.name

print(type(b), b)