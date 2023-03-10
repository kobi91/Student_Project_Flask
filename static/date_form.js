const date = document.getElementById("date");
const attendanceList = document.getElementById("attendanceList");

date.addEventListener("change", function() {
     const selectedDate = date.value;

     fetch(`/teacher/attendance_list?date=${selectedDate}`)
          .then(response => response.json())
          .then(data => {

               while (attendanceList.firstChild) {
                    attendanceList.removeChild(attendanceList.firstChild);
               }
               
               const newTrTh = document.createElement("tr");
               newTrTh.innerHTML = `<tr style="height:40px"><th>Number</th><th>Student Name</th><th>Course</th><th>${selectedDate}</th></tr>`;
               attendanceList.appendChild(newTrTh);

               data.forEach((student, index) => {
                    const newTrTd = document.createElement("tr");
                    newTrTd.innerHTML = `<tr><td>${index + 1}</td><td>${student[0]}</td><td>${student[1]}</td><td>${student[2]}</td></tr>`;                                   
                    attendanceList.appendChild(newTrTd);
               });
          }) 
          .catch(error => console.error(error));

});

function deleteTable() {
     const deleteDate = date.value;
     
     fetch('/teacher/attendance_list', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(deleteDate)
        })
        .then(response => response.json())
        .then(alert("The table has been deleted!"))
        .catch(error => console.error(error));
};





