const imageRoot = ReactDOM.createRoot(document.getElementById("images"));

function Images(props) {
    const [imageUrls, SetImageUrls] = React.useState([]);
    const [index, setIndex] = React.useState(0);

    React.useEffect(() => {
            axios.get("/images").then((response) => {
            SetImageUrls(response.data);   
            }) 
            .catch(error => console.error(error));       
    }, []);

    React.useEffect(() => {
        const changeImage = setInterval(() => {
            setIndex(currentIndex => (currentIndex + 1) % imageUrls.length);
        }, props.interval);

        return () => clearInterval(changeImage);

    }, [imageUrls.length]);

    return <div><img src={imageUrls[index]}/></div>   
   
};

imageRoot.render(<Images interval={10000}/>);        








       