document.getElementById("login-button").addEventListener("click", async () => {
    const response = await fetch("http://localhost:8000/auth/spotify");
    const data = await response.json();
    window.location.href = data.auth_url;
});

async function fetchTopTracks(timeRange) {
    try {
        const response = await fetch(`http://localhost:8000/top-tracks?time_range=${timeRange}`, {
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
    } catch (error) {
        console.error("Error fetching top tracks:", error);
    }
}

async function fetchTopSingers(timeRange) {
    try {
        const response = await fetch(`http://localhost:8000/top-singers?time_range=${timeRange}`, {
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
    } catch (error) {
        console.error("Error fetching top singers:", error);
    }
}

window.addEventListener("load", async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");
    
    if (code && !localStorage.getItem("access_token")) {
        try {
            const response = await fetch(`http://localhost:8000/auth/spotify/callback?code=${code}`);
            const data = await response.json();
            localStorage.setItem("access_token", data.access_token);
            
            // Remove the code from the URL
            window.history.replaceState({}, document.title, "/");
            
            // Initial data fetch
            await fetchTopTracks("short_term");
            await fetchTopSingers("short_term");
        } catch (error) {
            console.error("Error during authentication:", error);
        }
    } else if (localStorage.getItem("access_token")) {
        // If already authenticated, fetch data
        await fetchTopTracks("short_term");
        await fetchTopSingers("short_term");
    }
});
