function deleteNote(noteId) {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    fetch(`/delete-note/${noteId}`, {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken  // Include the CSRF token in the headers
        }
    }).then((response) => {
        if (response.ok) {
            window.location.href = "/my_notes";
        } else {
            console.error("Error deleting note:", response.statusText);
        }
    })
    .catch((error) => {
        console.error("Error:", error);
    });
}

function shareNote(noteId) {
    const shareUrl = `${window.location.origin}/share-note/${noteId}`;
    const noteContent = document.querySelector(`pre[data-note-id="${noteId}"]`).innerText;
    const text = `Check out this note: ${shareUrl}`;

    // If the Web Share API is available, use it
    if (navigator.share) {
        navigator.share({
            title: 'Note',
            text: text,
            url: shareUrl
        }).catch(console.error);
    } else {
        // Fallback: Show a prompt to copy the link
        const copyLink = prompt("Copy this link to share:", shareUrl);
        if (copyLink) {
            const shareContainer = document.createElement('div');
            shareContainer.style.position = 'fixed';
            shareContainer.style.top = '10%';
            shareContainer.style.left = '10%';
            shareContainer.style.right = '10%';
            shareContainer.style.zIndex = '1000';
            shareContainer.style.backgroundColor = 'white';
            shareContainer.style.padding = '20px';
            shareContainer.style.boxShadow = '0 0 10px rgba(0,0,0,0.1)';
            shareContainer.style.borderRadius = '8px';
            shareContainer.innerHTML = `
                <p>Copy this link to share: <a href="${shareUrl}" target="_blank">${shareUrl}</a></p>
                <button onclick="window.open('https://wa.me/?text=${encodeURIComponent(text)}', '_blank')">WhatsApp</button>
                <button onclick="window.open('https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}', '_blank')">X (Twitter)</button>
                <button onclick="window.open('https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}', '_blank')">Facebook</button>
                <button onclick="window.open('mailto:?subject=Check out this note&body=${encodeURIComponent(text)}')">Email</button>
                <button onclick="window.open('https://t.me/share/url?url=${encodeURIComponent(shareUrl)}&text=${encodeURIComponent(text)}', '_blank')">Telegram</button>
                <button onclick="window.open('https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(shareUrl)}', '_blank')">LinkedIn</button>
                <button onclick="window.open('https://discord.com/channels/@me?note=${encodeURIComponent(text)}', '_blank')">Discord</button>
                <button onclick="window.open('https://www.instagram.com/?url=${encodeURIComponent(shareUrl)}', '_blank')">Instagram</button>
                <button onclick="document.body.removeChild(shareContainer)">Close</button>
            `;
            document.body.appendChild(noteContent);
        }
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    const themeToggleButton = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme') || 'light';

    if (currentTheme === 'dark') {
        document.body.classList.add('dark-mode');
        themeToggleButton.textContent = 'Light Mode';
    } else {
        themeToggleButton.textContent = 'Dark Mode';
    }

    themeToggleButton.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');

        let theme = 'light';
        if (document.body.classList.contains('dark-mode')) {
            theme = 'dark';
            themeToggleButton.textContent = 'Light Mode';
        } else {
            themeToggleButton.textContent = 'Dark Mode';
        }
        localStorage.setItem('theme', theme);
    });
});

function openLogoutModal() {
    document.getElementById('logoutModal').classList.remove('hidden');
}

function closeLogoutModal() {
    document.getElementById('logoutModal').classList.add('hidden');
}

function sendEmail() {
    const form = document.getElementById('contactForm');
    const formData = new FormData(form);

    fetch('/send-email', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.text())
    .then(data => {
        alert('Email sent successfully!');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to send email.');
    });
}

document.getElementById('menu-toggle').addEventListener('click', function() {
    const menu = document.getElementById('menu');
    if (menu.classList.contains('hidden')) {
        menu.classList.remove('hidden');
    } else {
        menu.classList.add('hidden');
    }
});


// function sendResetEmail() {
//     const email = document.getElementById('email').value;

//     fetch('/forgot-password', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ email }),
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.error) {
//             alert(data.error);
//         } else {
//             alert('Password reset email sent!');
//         }
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });
// }
