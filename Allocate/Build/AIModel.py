#import library


class AIModel:
    def generateExamSchedule(startDate, endDate):
        import numpy as np
        import matplotlib.pyplot as plt
        import random
        import copy
        import sys
        import pandas as pd
        from collections import defaultdict
        import datetime
        from datetime import timedelta , datetime
        # Create a list to store student IDs
        student_ids = []

        # === First block: Cyber.xlsx and DataScience.xlsx ===
        file_paths = [
            "InputFiles/Cyber.xlsx",
            "InputFiles/DataScience.xlsx"
        ]

        for file_path in file_paths:
            excel_file = pd.ExcelFile(file_path)

            for sheet_name in excel_file.sheet_names:
                try:
                    df = excel_file.parse(sheet_name)

                    # Extract student ID from row 9 (index 8), column 16 (index 15)
                    student_id = df.iloc[8, 15]
                    student_ids.append(student_id)

                except Exception as e:
                    print(f"Skipped sheet '{sheet_name}' in file '{file_path}' due to error: {e}")
                    continue

        # === Second block: Students Registration.xlsx ===
        file_path = "InputFiles/Students Registration.xlsx"
        excel_file = pd.ExcelFile(file_path)

        for sheet_name in excel_file.sheet_names:
            df = excel_file.parse(sheet_name)

            # Extract student ID from row 10 (index 9) and column 11 (index 10)
            try:
                student_id = df.iloc[9, 11]  # Remember Python uses 0-based indexing
                student_ids.append(student_id)
            except IndexError:
                print(f"Skipped sheet '{sheet_name}' due to missing expected cell.")
                continue

        # === Print all results ===
        print("Extracted Student IDs:")
        for sid in student_ids:
            print(sid)

        print(f"\nTotal number of students: {len(student_ids)}")

        # Load the Excel file
        section_file = "InputFiles/Sem Courses.xlsx"
        df = pd.read_excel(section_file)

        # Loop through each row and check if 'lab' appears in any of the text columns
        lab_course_ids = set()

        for _, row in df.iterrows():
            course_id = str(row.iloc[0])
            # Check all cells for the word "lab"
            if row.astype(str).str.lower().str.contains("lab").any():
                lab_course_ids.add(course_id)

        # Print all detected lab course IDs
        print("Lab Courses ID:")
        for cid in lab_course_ids:
            print(cid)

        #assigning the lab exams to labs => 101-107 +PcLab =>done
        #fetch name lab and find it is course id =>done

        import pandas as pd
        from collections import defaultdict

        # === Settings ===
        start_date = startDate
        end_date = endDate
        excluded_courses = {"11391", "11494", "11493", "31160", "31251","14492","15491","15492","14391","15490","31160","36499"}

        lab_course_ids = {
            "21579", "22449", "12242", "15313", "27454", "14141", "22420", "24479", "22461", "22210",
            "15322", "22348", "15201", "23559", "24468", "22448", "11151", "11254", "20147", "27354",
            "25545", "22242", "21338", "25549", "21229", "24469", "36251", "24329", "15262", "15331",
            "11253", "14261", "27456", "14331", "21218", "21439", "11354", "20150", "14271", "21339",
            "11355", "23558", "15451", "25445", "36357", "27352", "36113", "27542"
        }

        student_files = [
            "InputFiles/Students Registration-old.xlsx",
            "InputFiles/Cyber.xlsx",
            "InputFiles/DataScience.xlsx"
        ]

        section_file = "InputFiles/Sem Courses.xlsx"
        room_file = "InputFiles/capacity-GP.xlsx"

        # === Prepare Dates ===
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        dates = [d for d in dates if d.weekday() != 4]  # Remove Fridays

        # Identify the first Saturday and get the next 6 non-Friday days from it
        first_saturday_index = next(i for i, d in enumerate(dates) if d.weekday() == 5)
        lab_period_dates = []
        i = first_saturday_index
        while len(lab_period_dates) < 7 and i < len(dates):
            if dates[i].weekday() != 4:
                lab_period_dates.append(dates[i])
            i += 1
        remaining_dates = [d for d in dates if d not in lab_period_dates]

        # === Step 1: Load Student-Course Registrations ===
        student_courses = {}

        for file_path in student_files:
            excel = pd.ExcelFile(file_path)
            for sheet_name in excel.sheet_names:
                df = excel.parse(sheet_name)
                try:
                    if "Students Registration-old" in file_path:
                        student_id = str(df.iloc[9, 11])
                        start_row = 14
                    else:
                        student_id = str(df.iloc[8, 15])
                        start_row = 13

                    course_ids = []
                    while start_row < len(df):
                        try:
                            course_id = df.iloc[start_row, 20]
                        except:
                            break
                        if pd.isna(course_id):
                            break
                        course_id = str(course_id)
                        if course_id not in excluded_courses:
                            course_ids.append(course_id)
                        start_row += 1

                    student_courses[student_id] = course_ids

                except Exception as e:
                    print(f"⚠️ Skipped '{sheet_name}' in '{file_path}' due to: {e}")
                    continue

        # === Step 2: Build Set of All Courses Taken ===
        all_courses = set()
        for courses in student_courses.values():
            all_courses.update(courses)

        # === Step 3: Load Sections ===
        sections_df = pd.read_excel(section_file)
        filtered_sections = sections_df[sections_df.iloc[:, 0].astype(str).isin(all_courses)]

        # === Build Course Sections: course_id → [students per section] ===
        course_sections = defaultdict(list)
        for _, row in filtered_sections.iterrows():
            course_id = str(row.iloc[0])
            course_sections[course_id].append(row.iloc[4])

        # === Build Course to Students Mapping ===
        course_students = defaultdict(list)
        for student_id, courses in student_courses.items():
            for course_id in courses:
                course_students[course_id].append(student_id)

        # === Step 4: Load Rooms ===
        rooms_df = pd.read_excel(room_file)
        rooms = sorted(zip(rooms_df.iloc[:, 0], rooms_df.iloc[:, 1]), key=lambda x: x[1])  # (room number, capacity)

        # Filter lab rooms and non-lab rooms
        lab_rooms = [(room, cap) for room, cap in rooms if (101 <= room <= 107) or (701 <= room <= 704)]
        non_lab_rooms = [room for room in rooms if room not in lab_rooms]

        # === Initialize ===
        schedule = []  # Final schedule list
        student_exam_days = defaultdict(list)  # student_id → list of exam dates
        exam_slots = defaultdict(list)  # (date, time) → list of course_ids assigned

        weekday_time_slots = ["15:00", "16:00", "17:00"]
        weekend_time_slots = ["8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]

        # Handling the structure Lab 11151
        def schedule_11151(course_id, sections, students):
            # Find the first Saturday in the lab period dates
            saturday = next((d for d in lab_period_dates if d.weekday() == 5), None)
            if not saturday:
                print("❌ No Saturday found for course 11151.")
                return

            # Define the 4 required consecutive times
            required_times = ["8:00", "9:00", "10:00", "11:00","12:00","1:00"]
            date_str = str(saturday.date())

            # Total rooms available
            total_rooms = lab_rooms.copy()
            total_sessions = len(required_times) * len(total_rooms)

            if len(sections) > total_sessions:
                print(f"❌ Not enough room-time slots to schedule all 23 sections of 11151.")
                return

            section_index = 0
            assigned_rooms = []

            for time in required_times:
                for room_no, capacity in total_rooms:
                    if section_index >= len(sections):
                        break

                    num_students = sections[section_index]

                    # Assign section to room and time
                    assigned_rooms.append((section_index + 1, room_no, time))
                    exam_slots[(date_str, time)].append(course_id)
                    section_index += 1

                if section_index >= len(sections):
                    break

            if section_index < len(sections):
                print("❌ Could not assign all sections of 11151 within 6 sessions.")
                return

            # Assign to schedule and update student exam tracking
            for student in students:
                student_exam_days[student].append(saturday.date())

            for section_idx, room, time in assigned_rooms:
                schedule.append((course_id, section_idx, room, date_str, time))

        ################################################################################################33


        def schedule_course(course_id, sections, students, valid_dates, valid_rooms):
            assigned = False
            best_slot = None
            min_conflicts = float('inf')

            for date in valid_dates:
                time_slots = weekend_time_slots if date.weekday() == 5 else weekday_time_slots
                for time in time_slots:
                    slot_key = (str(date.date()), time)
                    if len(exam_slots[slot_key]) >= 4:
                        continue
                    conflicts = sum(1 for student in students if student_exam_days[student].count(date.date()) >= 2)
                    if conflicts < min_conflicts:
                        min_conflicts = conflicts
                        best_slot = (date, time, slot_key)
                    if conflicts == 0:
                        break
                if best_slot and min_conflicts == 0:
                    break

            if not best_slot:
                print(f"❌ Could not assign course {course_id}.")
                for idx in range(len(sections)):
                    schedule.append((course_id, idx + 1, "❌ No Room", "⚠️ Failed", "-"))
                return

            date, time, slot_key = best_slot
            available_rooms = valid_rooms.copy()
            used_rooms = set()
            section_room_map = []
            fail = False

            for section_idx, num_students in enumerate(sections):
                room_assigned = False
                for room_no, capacity in available_rooms:
                    if room_no not in used_rooms and capacity >= num_students:
                        section_room_map.append((section_idx + 1, room_no))
                        used_rooms.add(room_no)
                        room_assigned = True
                        break
                if not room_assigned:
                    fail = True
                    break

            if fail:
                print(f"❌ Could not assign course {course_id}. No suitable room.")
                for idx in range(len(sections)):
                    schedule.append((course_id, idx + 1, "❌ No Room", "⚠️ Failed", "-"))
                return

            for student in students:
                student_exam_days[student].append(date.date())
            exam_slots[slot_key].append(course_id)

            for section_idx, room_no in section_room_map:
                schedule.append((course_id, section_idx, room_no, str(date.date()), time))

        # === Step 5: Enhanced Course Scheduler with Penalty Score ===
        def compute_penalty_score(students, exam_date):
            score = 0
            for student in students:
                exam_count = student_exam_days[student].count(exam_date)
                if exam_count >= 2:
                    score += 10  # heavy penalty for >2 exams (violates hard constraint)
                elif exam_count == 1:
                    score += 1  # mild penalty for 2 exams in one day (soft constraint)
            return score

        def schedule_course(course_id, sections, students, valid_dates, valid_rooms):
            best_slot = None
            lowest_penalty = float('inf')

            for date in valid_dates:
                time_slots = weekend_time_slots if date.weekday() == 5 else weekday_time_slots
                for time in time_slots:
                    slot_key = (str(date.date()), time)
                    if len(exam_slots[slot_key]) >= 4:
                        continue
                    penalty = compute_penalty_score(students, date.date())
                    if penalty < lowest_penalty:
                        lowest_penalty = penalty
                        best_slot = (date, time, slot_key)
                    if penalty == 0:
                        break
                if best_slot and lowest_penalty == 0:
                    break

            if not best_slot:
                print(f"❌ Could not assign course {course_id}.")
                for idx in range(len(sections)):
                    schedule.append((course_id, idx + 1, "❌ No Room", "⚠️ Failed", "-"))
                return

            date, time, slot_key = best_slot
            available_rooms = valid_rooms.copy()
            used_rooms = set()
            section_room_map = []
            fail = False

            for section_idx, num_students in enumerate(sections):
                room_assigned = False
                for room_no, capacity in available_rooms:
                    if room_no not in used_rooms and capacity >= num_students:
                        section_room_map.append((section_idx + 1, room_no))
                        used_rooms.add(room_no)
                        room_assigned = True
                        break
                if not room_assigned:
                    fail = True
                    break

            if fail:
                print(f"❌ Could not assign course {course_id}. No suitable room.")
                for idx in range(len(sections)):
                    schedule.append((course_id, idx + 1, "❌ No Room", "⚠️ Failed", "-"))
                return

            for student in students:
                student_exam_days[student].append(date.date())
            exam_slots[slot_key].append(course_id)

            for section_idx, room_no in section_room_map:
                schedule.append((course_id, section_idx, room_no, str(date.date()), time))

        # === Schedule Courses ===
        if "11151" in course_sections:
            sections = course_sections["11151"]
            students = course_students.get("11151", [])
            schedule_11151("11151", sections, students)

        for course_id, sections in course_sections.items():
            if course_id == "11151":
                continue
            students = course_students.get(course_id, [])
            if course_id in lab_course_ids:
                schedule_course(course_id, sections, students, lab_period_dates, lab_rooms)
            else:
                schedule_course(course_id, sections, students, remaining_dates, rooms)

        # === Final Output ===
        print("\n📅 Final Exam Schedule:")
        for course_id, section_idx, room, date, time in schedule:
            print(f"Course: {course_id} | Section {section_idx} → Room: {room} on {date} at {time}")

        # === Step 6: Final Output csv ===
        print("\n📅 Final Exam Schedule:")
        schedule_data = []  # For storing rows to be saved

        for course_id, section_idx, room, date, time in schedule:
            print(f"Course: {course_id} | Section {section_idx} → Room: {room} on {date} at {time}")
            schedule_data.append({
                "Course ID": course_id,
                "Section": section_idx,
                "Room": room,
                "Date": date,
                "Time": time
            })

        # Convert to DataFrame
        schedule_df = pd.DataFrame(schedule_data)

        # Save to CSV
        schedule_df.to_csv("outputFiles/ExamsSchedule.csv", index=False)

        # Print total number of courses the system is dealing with
        total_courses = len(course_sections)
        print(f"Total number of courses: {total_courses}")

        # Detect students with 2 exams on the same day
        from collections import Counter

        print("\n Students with 2 exams on the same day:")
        students_with_three_exams = set()

        for student_id, dates_list in student_exam_days.items():
            date_counts = Counter(dates_list)
            for exam_date, count in date_counts.items():
                if count == 2:
                    print(f"Student ID: {student_id} → 2 exams on {exam_date}")
                    students_with_three_exams.add(student_id)

        print(f"\n Total students with 2 exams on the same day: {len(students_with_three_exams)}")

        # Detect students with 3 exams on the same day
        from collections import Counter

        print("\n Students with 3 exams on the same day:")
        students_with_three_exams = set()

        for student_id, dates_list in student_exam_days.items():
            date_counts = Counter(dates_list)
            for exam_date, count in date_counts.items():
                if count == 3:
                    print(f"Student ID: {student_id} → 3 exams on {exam_date}")
                    students_with_three_exams.add(student_id)

        print(f"\n Total students with 3 exams on the same day: {len(students_with_three_exams)}")

        from collections import defaultdict

        # Step 1: Map course_id → (date, time)
        course_exam_time = {}
        for course_id, section_num, room, date, time in schedule:
            if course_id not in course_exam_time and date != "⚠️ Failed to schedule":
                course_exam_time[course_id] = (date, time)

        # Step 2: Build and print each student's schedule
        print("\n📚 Student Exam Schedules:\n")
        for student_id, courses in student_courses.items():
            print(f"🧑 Student ID: {student_id}")
            for course_id in courses:
                if course_id in course_exam_time:
                    date, time = course_exam_time[course_id]
                    print(f"   📘 Course ID: {course_id} → Exam on {date} at {time}")
                else:
                    print(f"   ⚠️ Course ID: {course_id} → Not scheduled yet")
            print("-" * 50)