document.getElementById('srt-icon').addEventListener('click', function () {
    var content = document.getElementById('translate-box').value;
    var blob = new Blob([content], { type: 'text/srt' });
    var a = document.createElement('a');
    a.href = window.URL.createObjectURL(blob);
    a.download = 'translated_transcripted_text.srt';
    a.click();
});

document.getElementById('srt-icon1').addEventListener('click', function () {
    var content = document.getElementById('Summarize-box').value;
    var blob = new Blob([content], { type: 'text/srt' });
    var a = document.createElement('a');
    a.href = window.URL.createObjectURL(blob);
    a.download = 'Summerized_text.srt';
    a.click();
});

document.getElementById('copy-icon').addEventListener('click', function () {
    var textArea = document.getElementById('translate-box');
    textArea.select();
    document.execCommand('copy');

    // Show notification
    var copyNotification = document.getElementById('copy-notification');
    copyNotification.style.display = 'block';
    setTimeout(function () {
        copyNotification.style.display = 'none';
    }, 2000);
});

document.getElementById('copy-icon1').addEventListener('click', function () {
    var textArea = document.getElementById('Summarize-box');
    textArea.select();
    document.execCommand('copy');

    // Show notification
    var copyNotification = document.getElementById('copy-notification');
    copyNotification.style.display = 'block';
    setTimeout(function () {
        copyNotification.style.display = 'none';
    }, 2000);
});

document.getElementById('share-icon').addEventListener('click', function () {
    var summarizeText = document.getElementById('Summarize-box').value;
    var dialogBox = document.getElementById('dialog-box');
    if (dialogBox.style.display === 'none') {
        dialogBox.style.display = 'block';
    } else {
        dialogBox.style.display = 'none';
    }
});

document.querySelectorAll('.social-icon').forEach(function (icon) {
    icon.addEventListener('click', function () {
        var socialMedia = this.alt;
        // Open the sharing page of the selected social media
        switch (socialMedia) {
            case 'Facebook':
                window.open('https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(window.location.href), '_blank');
                break;
            case 'Twitter':
                window.open('https://twitter.com/intent/tweet?url=' + encodeURIComponent(window.location.href), '_blank');
                break;
            case 'WhatsApp':
                window.open('https://api.whatsapp.com/send?text=' + encodeURIComponent(window.location.href), '_blank');
                break;
            case 'Telegram':
                window.open('https://telegram.me/share/url?url=' + encodeURIComponent(window.location.href), '_blank');
                break;
            case 'Instagram':
                window.open('https://www.instagram.com/', '_blank');
                break;
        }
    });
});




const textArea = document.getElementById('Summarize-box');
const downloadButton = document.getElementById('download-audio');



function playAndFetch() {
    playYouTubeVideo();
    //fetchTranscript();
}

function playYouTubeVideo() {
    const youtubeUrl = document.getElementById('youtube-url').value;
    const videoId = extractVideoId(youtubeUrl);
    console.log(videoId);
    
    if (videoId) {
        const iframeSrc = 'https://www.youtube.com/embed/' + videoId;
        document.getElementById('video-player').innerHTML = '<iframe class="video-iframe" src="' + iframeSrc + '" frameborder="0" allowfullscreen></iframe>';
        fetchTranscript(videoId);
    } else {
        alert('Invalid YouTube URL');
    }
}

function extractVideoId(url) {
    // Regex pattern to extract the video ID from the URL
    const pattern = /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;

    // Extract the video ID using the pattern
    const match = url.match(pattern);

    // Return the video ID if found, otherwise return null
    return match ? match[1] : null;
}

document.getElementById('submitbutton').addEventListener('click', function(event) {
    var selectedValue = document.getElementById('nativelanguage').value;
    if (selectedValue === '#') {
        event.preventDefault(); // Prevent button click default behavior
        alert('Please select your native language.'); // Display an alert or perform any other action
    }
});