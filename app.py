import streamlit as st
import pandas as pd

def main():
    # Page configuration
    st.set_page_config(
        page_title="IITK CPI Calculator",
        page_icon="🎓",
        layout="wide"
    )
    
    # Header
    st.title("🎓 IIT Kanpur CPI Calculator")
    st.markdown("---")
    
    # Grade point mapping
    grade_points = {
        "A+": 10,
        "A": 10,
        "B+": 9,
        "B": 8,
        "C+": 7,
        "C": 6,
        "D+": 5,
        "D": 4
    }
    
    # Sidebar for calculator type and semester selection
    with st.sidebar:
        st.header("🎯 Calculator Type")
        calc_type = st.radio(
            "Choose Calculator:",
            ["Single Semester CPI", "Overall CPI (Multiple Semesters)", "Quick CPI Calculator"],
            index=0
        )
        
        if calc_type == "Single Semester CPI":
            st.header("📚 Semester Details")
            semester = st.selectbox(
                "Select Semester:",
                options=list(range(1, 9)),
                format_func=lambda x: f"Semester {x}"
            )
            
            num_courses = st.number_input(
                "Number of Courses:",
                min_value=1,
                max_value=15,
                value=5,
                step=1
            )
        elif calc_type == "Overall CPI (Multiple Semesters)":
            st.header("📚 Overall CPI Details")
            num_semesters = st.number_input(
                "Number of Semesters:",
                min_value=1,
                max_value=8,
                value=2,
                step=1
            )
        else:  # Quick CPI Calculator
            st.header("⚡ Quick Calculator")
            num_subjects = st.number_input(
                "Number of Subjects:",
                min_value=1,
                max_value=20,
                value=5,
                step=1
            )
    
    # Main content area
    if calc_type == "Single Semester CPI":
        # Single Semester CPI Calculator
        st.header(f"Semester {semester} - Course Details")
        
        # Initialize session state for course data
        if 'courses' not in st.session_state:
            st.session_state.courses = []
        
        # Adjust courses list based on num_courses
        while len(st.session_state.courses) < num_courses:
            st.session_state.courses.append({'name': '', 'credit': 9, 'grade': 'A'})
        while len(st.session_state.courses) > num_courses:
            st.session_state.courses.pop()
        
        # Create columns for better layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Enter Course Information")
            
            # Course input form
            for i in range(num_courses):
                st.markdown(f"**Course {i+1}:**")
                cols = st.columns([3, 1, 1])
                
                with cols[0]:
                    course_name = st.text_input(
                        f"Course Name",
                        value=st.session_state.courses[i]['name'],
                        key=f"name_{i}",
                        placeholder=f"e.g., Mathematics-I, Physics-I"
                    )
                    st.session_state.courses[i]['name'] = course_name
                
                with cols[1]:
                    credit = st.number_input(
                        f"Credits",
                        min_value=1,
                        max_value=10,
                        value=st.session_state.courses[i]['credit'],
                        key=f"credit_{i}"
                    )
                    st.session_state.courses[i]['credit'] = credit
                
                with cols[2]:
                    grade = st.selectbox(
                        f"Grade",
                        options=list(grade_points.keys()),
                        index=list(grade_points.keys()).index(st.session_state.courses[i]['grade']),
                        key=f"grade_{i}"
                    )
                    st.session_state.courses[i]['grade'] = grade
                
                st.markdown("---")
        
        with col2:
            st.subheader("Grade Point Scale")
            grade_df = pd.DataFrame([
                {"Grade": grade, "Points": points} 
                for grade, points in grade_points.items()
            ])
            st.dataframe(grade_df, use_container_width=True)
            
            # Calculate CPI button
            if st.button("🧮 Calculate CPI", type="primary", use_container_width=True):
                total_grade_points = 0
                total_credits = 0
                
                # Calculate CPI
                for course in st.session_state.courses:
                    if course['name']:  # Only include courses with names
                        grade_point = grade_points[course['grade']]
                        credit = course['credit']
                        total_grade_points += grade_point * credit
                        total_credits += credit
                
                if total_credits > 0:
                    cpi = total_grade_points / total_credits
                    
                    # Display results
                    st.success(f"**Your CPI: {cpi:.2f}**")
                    
                    # Performance indicator
                    if cpi >= 9.0:
                        st.balloons()
                        st.success("🌟 Outstanding Performance!")
                    elif cpi >= 8.0:
                        st.success("🎉 Excellent Performance!")
                    elif cpi >= 7.0:
                        st.info("👍 Good Performance!")
                    elif cpi >= 6.0:
                        st.warning("📈 Average Performance - Keep improving!")
                    else:
                        st.error("📚 Need more effort - You can do better!")
                else:
                    st.error("Please enter at least one course with a name!")
        
        # Detailed breakdown for single semester
        if st.button("📊 Show Detailed Breakdown"):
            st.subheader("Detailed Calculation Breakdown")
            
            breakdown_data = []
            total_grade_points = 0
            total_credits = 0
            
            for i, course in enumerate(st.session_state.courses):
                if course['name']:
                    grade_point = grade_points[course['grade']]
                    credit = course['credit']
                    weighted_points = grade_point * credit
                    
                    breakdown_data.append({
                        "Course": course['name'] or f"Course {i+1}",
                        "Credits": credit,
                        "Grade": course['grade'],
                        "Grade Points": grade_point,
                        "Weighted Points": weighted_points
                    })
                    
                    total_grade_points += weighted_points
                    total_credits += credit
            
            if breakdown_data:
                df = pd.DataFrame(breakdown_data)
                st.dataframe(df, use_container_width=True)
                
                # Summary
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Credits", total_credits)
                with col2:
                    st.metric("Total Grade Points", f"{total_grade_points:.1f}")
                with col3:
                    cpi = total_grade_points / total_credits if total_credits > 0 else 0
                    st.metric("Final CPI", f"{cpi:.2f}")
                
                # Formula explanation
                st.subheader("📐 Formula Used")
                st.latex(r"CPI = \frac{\sum (Grade\_Points \times Credits)}{\sum Credits}")
                st.write(f"CPI = {total_grade_points:.1f} ÷ {total_credits} = **{cpi:.2f}**")

    elif calc_type == "Overall CPI (Multiple Semesters)":
        # Overall CPI Calculator
        st.header(f"Overall CPI Calculator - {num_semesters} Semesters")
        
        # Initialize session state for semester data
        if 'semesters' not in st.session_state:
            st.session_state.semesters = []
        
        # Adjust semesters list based on num_semesters
        while len(st.session_state.semesters) < num_semesters:
            st.session_state.semesters.append({'name': f'Semester {len(st.session_state.semesters) + 1}', 'cpi': 9.0, 'credits': 36})
        while len(st.session_state.semesters) > num_semesters:
            st.session_state.semesters.pop()
        
        # Create columns for better layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Enter Semester-wise CPI and Credits")
            st.info("💡 Enter the CPI and total credits for each semester to calculate overall CPI")
            
            # Semester input form
            for i in range(num_semesters):
                st.markdown(f"**{st.session_state.semesters[i]['name']}:**")
                cols = st.columns([2, 1, 1])
                
                with cols[0]:
                    sem_name = st.text_input(
                        f"Semester Name",
                        value=st.session_state.semesters[i]['name'],
                        key=f"sem_name_{i}",
                        placeholder=f"e.g., Semester {i+1}, Summer Term"
                    )
                    st.session_state.semesters[i]['name'] = sem_name
                
                with cols[1]:
                    sem_cpi = st.number_input(
                        f"CPI",
                        min_value=0.0,
                        max_value=10.0,
                        value=float(st.session_state.semesters[i]['cpi']),
                        step=0.01,
                        format="%.2f",
                        key=f"sem_cpi_{i}"
                    )
                    st.session_state.semesters[i]['cpi'] = sem_cpi
                
                with cols[2]:
                    sem_credits = st.number_input(
                        f"Credits",
                        min_value=1,
                        max_value=50,
                        value=st.session_state.semesters[i]['credits'],
                        key=f"sem_credits_{i}"
                    )
                    st.session_state.semesters[i]['credits'] = sem_credits
                
                st.markdown("---")
        
        with col2:
            st.subheader("Grade Point Scale")
            grade_df = pd.DataFrame([
                {"Grade": grade, "Points": points} 
                for grade, points in grade_points.items()
            ])
            st.dataframe(grade_df, use_container_width=True)
            
            # Calculate Overall CPI button
            if st.button("🧮 Calculate Overall CPI", type="primary", use_container_width=True):
                total_weighted_cpi = 0
                total_credits = 0
                
                # Calculate Overall CPI
                for semester in st.session_state.semesters:
                    if semester['name'] and semester['cpi'] > 0:
                        weighted_cpi = semester['cpi'] * semester['credits']
                        total_weighted_cpi += weighted_cpi
                        total_credits += semester['credits']
                
                if total_credits > 0:
                    overall_cpi = total_weighted_cpi / total_credits
                    
                    # Display results
                    st.success(f"**Your Overall CPI: {overall_cpi:.2f}**")
                    
                    # Performance indicator
                    if overall_cpi >= 9.0:
                        st.balloons()
                        st.success("🌟 Outstanding Overall Performance!")
                    elif overall_cpi >= 8.0:
                        st.success("🎉 Excellent Overall Performance!")
                    elif overall_cpi >= 7.0:
                        st.info("👍 Good Overall Performance!")
                    elif overall_cpi >= 6.0:
                        st.warning("📈 Average Performance - Keep improving!")
                    else:
                        st.error("📚 Need more effort - You can do better!")
                else:
                    st.error("Please enter valid CPI and credits for at least one semester!")
        
        # Detailed breakdown for overall CPI
        if st.button("📊 Show Overall CPI Breakdown"):
            st.subheader("Overall CPI Calculation Breakdown")
            
            breakdown_data = []
            total_weighted_cpi = 0
            total_credits = 0
            
            for semester in st.session_state.semesters:
                if semester['name'] and semester['cpi'] > 0:
                    weighted_cpi = semester['cpi'] * semester['credits']
                    
                    breakdown_data.append({
                        "Semester": semester['name'],
                        "CPI": f"{semester['cpi']:.2f}",
                        "Credits": semester['credits'],
                        "Weighted CPI": f"{weighted_cpi:.2f}"
                    })
                    
                    total_weighted_cpi += weighted_cpi
                    total_credits += semester['credits']
            
            if breakdown_data:
                df = pd.DataFrame(breakdown_data)
                st.dataframe(df, use_container_width=True)
                
                # Summary
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Credits", total_credits)
                with col2:
                    st.metric("Total Weighted CPI", f"{total_weighted_cpi:.2f}")
                with col3:
                    overall_cpi = total_weighted_cpi / total_credits if total_credits > 0 else 0
                    st.metric("Overall CPI", f"{overall_cpi:.2f}")
                
                # Formula explanation
                st.subheader("📐 Formula Used")
                st.latex(r"Overall\_CPI = \frac{\sum (Semester\_CPI \times Credits)}{\sum Credits}")
                st.write(f"Overall CPI = {total_weighted_cpi:.2f} ÷ {total_credits} = **{overall_cpi:.2f}**")

    else:  # Quick CPI Calculator
        # Quick CPI Calculator
        st.header(f"⚡ Quick CPI Calculator - {num_subjects} Subjects")
        
        # Initialize session state for quick subjects data
        if 'quick_subjects' not in st.session_state:
            st.session_state.quick_subjects = []
        
        # Adjust subjects list based on num_subjects
        while len(st.session_state.quick_subjects) < num_subjects:
            st.session_state.quick_subjects.append({'credit': 9, 'grade': 'A'})
        while len(st.session_state.quick_subjects) > num_subjects:
            st.session_state.quick_subjects.pop()
        
        # Create columns for better layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Enter Credits and Grades Only")
            st.info("💡 Simple & Fast - Just enter credits and grades for each subject!")
            
            # Quick subject input form
            for i in range(num_subjects):
                st.markdown(f"**Subject {i+1}:**")
                cols = st.columns([1, 1])
                
                with cols[0]:
                    credit = st.number_input(
                        f"Credits",
                        min_value=1,
                        max_value=10,
                        value=st.session_state.quick_subjects[i]['credit'],
                        key=f"quick_credit_{i}"
                    )
                    st.session_state.quick_subjects[i]['credit'] = credit
                
                with cols[1]:
                    grade = st.selectbox(
                        f"Grade",
                        options=list(grade_points.keys()),
                        index=list(grade_points.keys()).index(st.session_state.quick_subjects[i]['grade']),
                        key=f"quick_grade_{i}"
                    )
                    st.session_state.quick_subjects[i]['grade'] = grade
                
                st.markdown("---")
        
        with col2:
            st.subheader("Grade Point Scale")
            grade_df = pd.DataFrame([
                {"Grade": grade, "Points": points} 
                for grade, points in grade_points.items()
            ])
            st.dataframe(grade_df, use_container_width=True)
            
            # Calculate Quick CPI button
            if st.button("⚡ Calculate CPI", type="primary", use_container_width=True):
                total_grade_points = 0
                total_credits = 0
                
                # Calculate CPI
                for subject in st.session_state.quick_subjects:
                    grade_point = grade_points[subject['grade']]
                    credit = subject['credit']
                    total_grade_points += grade_point * credit
                    total_credits += credit
                
                if total_credits > 0:
                    cpi = total_grade_points / total_credits
                    
                    # Display results
                    st.success(f"**Your CPI: {cpi:.2f}**")
                    
                    # Performance indicator
                    if cpi >= 9.0:
                        st.balloons()
                        st.success("🌟 Outstanding Performance!")
                    elif cpi >= 8.0:
                        st.success("🎉 Excellent Performance!")
                    elif cpi >= 7.0:
                        st.info("👍 Good Performance!")
                    elif cpi >= 6.0:
                        st.warning("📈 Average Performance - Keep improving!")
                    else:
                        st.error("📚 Need more effort - You can do better!")
        
        # Detailed breakdown for quick calculator
        if st.button("📊 Show Quick Breakdown"):
            st.subheader("Quick Calculation Breakdown")
            
            breakdown_data = []
            total_grade_points = 0
            total_credits = 0
            
            for i, subject in enumerate(st.session_state.quick_subjects):
                grade_point = grade_points[subject['grade']]
                credit = subject['credit']
                weighted_points = grade_point * credit
                
                breakdown_data.append({
                    "Subject": f"Subject {i+1}",
                    "Credits": credit,
                    "Grade": subject['grade'],
                    "Grade Points": grade_point,
                    "Weighted Points": weighted_points
                })
                
                total_grade_points += weighted_points
                total_credits += credit
            
            if breakdown_data:
                df = pd.DataFrame(breakdown_data)
                st.dataframe(df, use_container_width=True)
                
                # Summary
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Credits", total_credits)
                with col2:
                    st.metric("Total Grade Points", f"{total_grade_points:.1f}")
                with col3:
                    cpi = total_grade_points / total_credits if total_credits > 0 else 0
                    st.metric("Final CPI", f"{cpi:.2f}")
                
                # Formula explanation
                st.subheader("📐 Formula Used")
                st.latex(r"CPI = \frac{\sum (Grade\_Points \times Credits)}{\sum Credits}")
                st.write(f"CPI = {total_grade_points:.1f} ÷ {total_credits} = **{cpi:.2f}**")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            <p>🏛️ IIT Kanpur CPI Calculator | Made with ❤️ using Streamlit</p>
            <p><small>✨ Features: Single Semester CPI, Overall CPI & Quick CPI Calculator</small></p>
            <p><small>Note: This calculator follows the standard IITK grading system</small></p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()