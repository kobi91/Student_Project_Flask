const course = document.getElementById("course");
const studentsList = document.getElementById("studentsList");

course.addEventListener("change", function() {
     const selectedCourse = course.value;

     fetch(`/teacher/course_attendance?course=${selectedCourse}`)
          .then(response => response.json())
          .then(data => {

               while (studentsList.firstChild) {
                    studentsList.removeChild(studentsList.firstChild);
               }
               
               data.forEach((student, index) => {
                    const radioId = `radio-${index + 1}`;
                    const newLi = document.createElement("li");
                    newLi.setAttribute("id", radioId)
                    newLi.innerHTML = `
                    <a class="bold">${student}</a>
                    <label for="Yes">Yes</label>
                    <input type="radio" id="Yes" value="Yes" name='${student}' checked>
                    <label for="No">No</label>   
                    <input type="radio" id="No" value="No" name='${student}'> 
                    <button type="button" onclick="submitAttendance('${radioId}')" class="btn">Set</button><br>
                    `;
                    studentsList.appendChild(newLi)
               });
          }) 
          .catch(error => console.error(error));

});

function submitAttendance(radioId) {
     const radio = document.getElementById(radioId);
     const radioInputs = radio.getElementsByTagName("input");
     let value = null;
     let name = null;

     for (let i = 0; i < radioInputs.length; i++) {
          if (radioInputs[i].checked) {
               value = radioInputs[i].value;
               name = radioInputs[i].name;
               break;
          }
     }
     
     fetch(`/teacher/attendance?attendance=${[value, name]}`)    
           .then(response => response.json())
           .catch(error => console.error(error));
};



