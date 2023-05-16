const messageRoot = ReactDOM.createRoot(document.getElementById("messages"));
let messages = [];
let generator = "";
let a = 100;
const c = 5000;
let b = 100;
let GenerateInterval = setInterval(generate, b);
let DataInterval = setInterval(renderData, a);

setTimeout(() =>{
    clearInterval(GenerateInterval);
    clearInterval(DataInterval);
    a = 10000;
    b = a * messages.length;
    GenerateInterval = setInterval(generate, b);
    DataInterval = setInterval(renderData, a); 
}, 200);

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
    messageRoot.render(<MessagesList/>);        
}

getData();
setInterval(getData, c);

generate();

