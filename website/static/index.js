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

document.addEventListener('DOMContentLoaded', () => {
    const notes = document.querySelectorAll('.note-content');

    notes.forEach(note => {
        const linesToShow = 5;
        const lineHeight = parseInt(getComputedStyle(note).lineHeight);
        const maxHeight = linesToShow * lineHeight;

        if (note.scrollHeight > maxHeight) {
            note.style.maxHeight = `${maxHeight}px`;
            note.style.overflow = 'hidden';

            const readMore = document.createElement('span');
            readMore.innerText = '...Read More';
            readMore.style.color = 'blue';
            readMore.style.cursor = 'pointer';
            note.parentNode.appendChild(readMore);

            // Add a click event listener to redirect to the full note page
            readMore.addEventListener('click', () => {
                const noteId = note.getAttribute('data-note-id');
                window.location.href = `/note/${noteId}`;
            });
        }
    });
});


function toggleMenu(button) {
    const dropdown = button.nextElementSibling;
    dropdown.classList.toggle('hidden');
}

// Optional: Close the menu if clicked outside
document.addEventListener('click', function (event) {
    const isClickInside = event.target.closest('.menu-container');

    if (!isClickInside) {
        const dropdowns = document.querySelectorAll('.menu-dropdown');
        dropdowns.forEach(dropdown => {
            dropdown.classList.add('hidden');
        });
    }
});


document.addEventListener('DOMContentLoaded', () => {
    // Ensure each note has its original text stored when the page loads
    document.querySelectorAll('.note-content, #note-content').forEach(noteElement => {
        noteElement.setAttribute('data-original-text', noteElement.textContent);
        noteElement.setAttribute('data-edited-text', noteElement.textContent); // Track edited state
    });
});

function makeEditable(noteElement, editButtons) {
    noteElement.contentEditable = 'true';
    noteElement.style.border = '1px solid #ccc';
    noteElement.focus();
    editButtons.classList.remove('hidden');
}

function makeNonEditable(noteElement, editButtons) {
    noteElement.contentEditable = 'false';
    noteElement.style.border = 'none';
    editButtons.classList.add('hidden');
}

function editNote(noteId) {
    const noteElement = getNoteElement(noteId);
    const editButtons = getEditButtons(noteElement);

    if (noteElement.isContentEditable) {
        // Save changes before making the note non-editable
        saveNoteChanges(noteId);
        makeNonEditable(noteElement, editButtons);
    } else {
        // Update the edited text before making the note editable
        noteElement.setAttribute('data-edited-text', noteElement.textContent);
        makeEditable(noteElement, editButtons);
    }
}

function saveNoteChanges(noteId) {
    const noteElement = getNoteElement(noteId);
    const updatedText = noteElement.textContent;

    // Fetch CSRF token
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // Send AJAX request to save changes
    fetch(`/update-note/${noteId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ data: updatedText }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Note updated successfully:', data);
        // Update the original and edited text after saving
        noteElement.setAttribute('data-original-text', updatedText);
        noteElement.setAttribute('data-edited-text', updatedText);
        makeNonEditable(noteElement, getEditButtons(noteElement));
    })
    .catch(error => {
        console.error('Error updating note:', error);
    });
}

function discardChanges(noteId) {
    const noteElement = getNoteElement(noteId);
    // Revert to the last saved state
    const originalText = noteElement.getAttribute('data-original-text');
    noteElement.textContent = originalText;
    noteElement.setAttribute('data-edited-text', originalText); // Update edited text
    makeNonEditable(noteElement, getEditButtons(noteElement));
}

function getNoteElement(noteId) {
    // Get the note element based on whether we're on a detail page or a list page
    const noteElement = document.querySelector(`.note-content[data-note-id="${noteId}"], #note-content[data-note-id="${noteId}"]`);
    return noteElement;
}

function getEditButtons(noteElement) {
    // Assuming edit buttons are siblings of the note element or inside a container
    let editButtons;
    if (noteElement.id === 'note-content') {
        editButtons = document.getElementById('edit-buttons');
    } else {
        const noteCard = noteElement.closest('.note-card');
        editButtons = noteCard.querySelector('.edit-buttons');
    }
    return editButtons;
}
