document.getElementById("login-button").addEventListener("click", async () => {
    const response = await fetch("/auth/spotify");
    const data = await response.json();
    window.location.href = data.auth_url;
});

async function fetchTopTracks(timeRange) {
    const response = await fetch(`/top-tracks?time_range=${timeRange}`, {
        headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
    });
    const data = await response.json();
    const tracksList = document.getElementById("tracks-list");
    tracksList.innerHTML = "";
    data.items.forEach((track) => {
        const listItem = document.createElement("li");
        listItem.textContent = `${track.name} by ${track.artists.map((artist) => artist.name).join(", ")}`;
        tracksList.appendChild(listItem);
    });
}

async function fetchTopSingers(timeRange) {
    const response = await fetch(`/top-singers?time_range=${timeRange}`, {
        headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
    });
    const data = await response.json();
    const singersList = document.getElementById("singers-list");
    singersList.innerHTML = "";
    data.items.forEach((singer) => {
        const listItem = document.createElement("li");
        listItem.textContent = singer.name;
        singersList.appendChild(listItem);
    });
}

window.addEventListener("load", async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const accessToken = urlParams.get("access_token");
    if (accessToken) {
        localStorage.setItem("access_token", accessToken);
        await fetchTopTracks("short_term");
        await fetchTopSingers("short_term");
    }
});
