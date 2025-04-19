# SwiftSign API Integration & Completion Plan (April 2025)

## 1. API Endpoint Mapping & Consistency

- [x] **Teacher Login**
  - Frontend: `/api/teacher_login` (POST)
  - Backend: `/api/teachers/login` (POST)
  - **Action:** Update frontend to use `/api/teachers/login`.

- [x] **Student Login**
  - Frontend: `/api/student_login` (POST)
  - Backend: `/api/students/login` (POST)
  - **Action:** Update frontend to use `/api/students/login`.

- [x] **Student Registration**
  - Frontend: `/api/student_register` (POST)
  - Backend: `/api/students` (POST)
  - **Action:** Update frontend to use `/api/students`.

- [x] **Student Photo Registration**
  - Frontend: `/api/student_register_photo` (POST)
  - Backend: `/api/students/<int:student_id>/photo` (POST)
  - **Action:** Update frontend to send student ID and use correct endpoint.

- [x] **Attendance Start/End**
  - Frontend: Implemented
  - Backend: `/api/attendance-sessions` (POST), `/api/attendance-sessions/current/end` (POST)
  - **Action:** Implemented frontend fetch for these endpoints.

- [x] **Attendance Table (Get Students)**
  - Frontend: `/api/attendance_students` (GET)
  - Backend: `/api/attendance-sessions/current/students` (GET)
  - **Action:** Updated frontend to use `/api/attendance-sessions/current/students`.

- [x] **Mark Attendance**
  - Frontend: `/api/mark_attendance` (POST)
  - Backend: `/api/attendance-sessions/current/students/<int:student_id>` (PATCH)
  - **Action:** Updated frontend to use PATCH and correct endpoint.

- [x] **Student Self-Attendance**
  - Frontend: `/api/attendanceRecord` (POST)
  - Backend: `/api/attendance-records` (POST)
  - **Action:** Updated frontend to use `/api/attendance-records`.

---

## 2. Backend Completion Checklist

- [x] **Filter students by group/module** in attendance session start endpoint.
- [x] **Face recognition logic** for student self-attendance (compare captured photo to stored vector).
- [ ] **Store attendance records** in DB (currently in-memory only).
- [ ] **Export attendance as Excel** (add endpoint and frontend button).
- [x] **Session status and timer**: ensure session state is robust.
- [x] **Error handling and messages**: unify error responses.

---

## 3. Frontend Integration Checklist

- [x] Update all fetch URLs to match backend endpoints above.
- [x] Use correct HTTP methods (POST, PATCH, GET).
- [x] Add comments to all API calls for clarity.
- [x] Implement start/end attendance session buttons (teacher dashboard).
- [ ] Implement Excel export button (teacher dashboard).
- [x] Ensure all error/success messages are user-friendly.

---

## 4. Documentation & Collaboration

- All changes will be commented in code and documented here.
- Use this plan as a living document: update as you work or as requirements change.
- Mark any TODOs or blockers here for team visibility.

---

## 5. Next Steps

1. ✅ Update frontend fetches to match backend endpoints.
2. ✅ Complete backend logic for filtering, face recognition, and DB storage.
3. ⏳ Implement Excel export and robust session management.
4. ⏳ Test end-to-end and document any issues or improvements needed.

---

## 6. Testing Instructions

### Teacher Flow
1. Login as a teacher using email ending with `@hns-re2sd.dz` (e.g., `teacher@hns-re2sd.dz`)
2. Teacher dashboard will load with your subjects in the dropdown
3. Select a subject and group, then click "Start Attendance"
4. Students table will populate with students from that class
5. Mark students as present/absent manually or wait for student self-attendance
6. Click "End Attendance" when done

### Student Flow
1. Teacher must start an attendance session first
2. Login as a student with email ending with `@hns-re2sd.dz` (e.g., `student@hns-re2sd.dz`)
3. You will only be able to login if you belong to the class for the current session
4. Take a photo for face verification
5. Submit attendance

### Registration Flow
1. Open registration page
2. Fill in name, class, and email (ending with `@hns-re2sd.dz`)
3. Take a photo for face recognition
4. Your account will be created

### Future Enhancements
- Add permanent database storage for attendance records
- Implement Excel export functionality
- Add detailed reporting and statistics

---

# user notes on the plan change (April 19, 2025)

- In the frontend, the teacher will have a dropdown menu for subject selection, showing only the subjects they teach (fetched from the backend after login). ✅
- When a student tries to log in, verify that they belong to the class/group for which the teacher has started the attendance session. Block or show an error if not. ✅
- Update the teacher dashboard style to match the style and UX of the other pages (consistent colors, layout, dark mode, etc). ✅
- When the teacher starts an attendance session, fetch only the students in the selected class/group/subject and display them in the dashboard table. The table should update in real time as attendance is marked. ✅