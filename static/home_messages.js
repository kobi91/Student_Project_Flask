let messages = [];
let generator = "";
const a = 10000;
const c = 5000;
let b = 5000;
let myInterval = setInterval(generate, b);


setTimeout(() =>{
    clearInterval(myInterval);
    b = a * messages.length;
    myInterval = setInterval(generate, b); 
}, 6000);

function generate() {
  generator = generateValues(messages);  
}

function* generateValues(values) {
    for (let i = 0; i < values.length; i++) {
        yield values[i];
    }
}

function MessagesList() {
    return (  
        <p>{generator.next().value}</p>  
    );
}

function getData() {  
    axios.get("/messages").then((response) => {
    messages = response.data;
    }) 
   .catch(error => console.error(error));     
}

function renderData() { 
    ReactDOM.render(<MessagesList messages = {messages}/>, document.getElementById("messages"));         
}

getData();
setInterval(getData, c);

generate();

renderData();
setInterval(renderData, a);
