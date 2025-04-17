function search() {
    let keyword = document.getElementById("keyword").value;
    let api = `http://127.0.0.1:5000/search/${keyword}`;
    fetch(api)
        .then(response => response.json())
        .then(data => {
            let result = document.getElementById("results");
            result.innerHTML = ""; // Clear previous results
            for(let i = 1; i < Object.keys(data).length; i++){
                let div = document.createElement("div");
                div.className = "game";
                div.innerHTML = `<a href='${data[i].link}' target='_blank'><h3>チーム名：${data[i].teamname}</h3><p>参加条件：${data[i].requirements}</p><p>開催時間：${data[i].time}</p><p>場所：${data[i].address}</p></a>`;
                result.appendChild(div);
            }
        })
        .catch(error => console.error('Error:', error));
}
