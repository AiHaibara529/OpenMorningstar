const endpoint = "https://youtube-homepage-clone.vercel.app/js/data.json"
let videoList;

fetch(endpoint)
	.then(blob => blob.json())
	.then(data => {
		videoList = data.items
		videoList.forEach(video => {
			console.log(video)
		});
	})
