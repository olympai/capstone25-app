import { renderFile } from '../preview.js';

$(document).ready(function () {
    // File Upload in Offcanvas
    // Drag and Drop Field
    const dropzone = document.getElementById("dropzone");
    const fileInput = document.getElementById("vfgert");
    const fileList = document.getElementById("file-list");

    // Öffnet den Datei-Dialog beim Klicken auf die Dropzone
    dropzone.addEventListener("click", () => fileInput.click());

    // Verhindert Standardverhalten beim Draggen
    dropzone.addEventListener("dragover", (event) => {
        event.preventDefault();
        dropzone.classList.add("dragover");
    });

    dropzone.addEventListener("dragleave", () => {
        dropzone.classList.remove("dragover");
    });

    // Function to validate document file type
    function isValidDocumentFile(file) {
        const validExtensions = ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.xls', '.pptx', '.ppt', '.csv', '.rtf', '.odt', '.ods', '.odp'];
        const fileName = file.name.toLowerCase();
        const isValidExtension = validExtensions.some(ext => fileName.endsWith(ext));
        // Also accept common document MIME types
        const validMimeTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument', 'text/plain', 'text/csv', 'application/vnd.ms-excel', 'application/vnd.ms-powerpoint'];
        const isValidMimeType = validMimeTypes.some(type => file.type.startsWith(type));
        return isValidExtension || isValidMimeType;
    }

    // Function to validate file size (max 25MB)
    function isValidFileSize(file) {
        const maxSize = 25 * 1024 * 1024; // 25MB in bytes
        return file.size <= maxSize;
    }

    // Function to format file size for display
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }

    // Dateien beim Drop ins Input-Feld schreiben
    dropzone.addEventListener("drop", (event) => {
        event.preventDefault();
        dropzone.classList.remove("dragover");

        if (event.dataTransfer.files.length > 0) {
            // Validate all files
            const files = Array.from(event.dataTransfer.files);
            const invalidFiles = files.filter(file => !isValidDocumentFile(file));
            const oversizedFiles = files.filter(file => !isValidFileSize(file));

            if (invalidFiles.length > 0) {
                alert(`The following file types are not allowed: ${invalidFiles.map(f => f.name).join(', ')}\n\nSupported formats: PDF, DOCX, DOC, TXT, XLSX, XLS, PPTX, PPT, CSV, RTF, ODT, ODS, ODP`);
                return;
            }

            if (oversizedFiles.length > 0) {
                alert(`The following files are too large (max 25MB):\n${oversizedFiles.map(f => `${f.name} (${formatFileSize(f.size)})`).join('\n')}`);
                return;
            }

            fileInput.files = event.dataTransfer.files; // Dateien ins Input setzen
            displayFiles(event.dataTransfer.files);
        }
    });

    // Event-Listener für direktes Datei-Input (wenn per Klick hochgeladen wird)
    fileInput.addEventListener("change", (event) => {
        console.log('Files:', event.target.files);

        // Validate all files
        const files = Array.from(event.target.files);
        const invalidFiles = files.filter(file => !isValidDocumentFile(file));
        const oversizedFiles = files.filter(file => !isValidFileSize(file));

        if (invalidFiles.length > 0) {
            alert(`The following file types are not allowed: ${invalidFiles.map(f => f.name).join(', ')}\n\nSupported formats: PDF, DOCX, DOC, TXT, XLSX, XLS, PPTX, PPT, CSV, RTF, ODT, ODS, ODP`);
            fileInput.value = ''; // Clear input
            return;
        }

        if (oversizedFiles.length > 0) {
            alert(`The following files are too large (max 25MB):\n${oversizedFiles.map(f => `${f.name} (${formatFileSize(f.size)})`).join('\n')}`);
            fileInput.value = ''; // Clear input
            return;
        }

        displayFiles(event.target.files);
    })

    // Funktion zur Anzeige der hochgeladenen Dateien
    function displayFiles(files) {
        fileList.innerHTML = ""; // Vorherige Liste leeren
        Array.from(files).forEach((file, index) => {
            const listItem = document.createElement("li");
            listItem.innerHTML = `${file.name} <span class="remove-file" data-index="${index}"><i class="bi bi-x-lg"></i></span>`;
            fileList.appendChild(listItem);
        });

        // Event-Listener zum Entfernen von Dateien
        document.querySelectorAll(".remove-file").forEach((button) => {
            button.addEventListener("click", function () {
                const index = this.getAttribute("data-index");
                removeFile(index);
            });
        });
    }

    // Funktion zum Entfernen von Dateien aus der Liste
    function removeFile(index) {
        let dt = new DataTransfer();
        let files = fileInput.files;
        for (let i = 0; i < files.length; i++) {
            if (i != index) {
                dt.items.add(files[i]); // Alle außer der entfernten Datei hinzufügen
            }
        }
        fileInput.files = dt.files; // Neues FileList-Objekt setzen
        displayFiles(fileInput.files); // Liste aktualisieren
    }


    // append loader
    document.getElementById('upload_button').addEventListener("click", function() {
        var loader = '<div class="alert alert-dark d-flex align-items-center" style="margin-top: 10px;" role="alert">' +
                    '<div class="spinner-border text-dark me-3" role="status">' +
                        '<span class="visually-hidden">Loading...</span>' +
                    '</div>' +
                    '<b class="me-3">Uploading ...</b>' +
                    '</div>';
        document.getElementById('loading_bar').innerHTML = loader;  
    });


    // Event Delegation für alle dynamischen Buttons mit der Klasse 'fetchfile'
    document.addEventListener("click", function (event) {
        const button = event.target.closest(".fetchfile"); // Prüft, ob ein Element mit der Klasse geklickt wurde
        if (!button) return; // Falls es kein fetchfile-Button ist, nichts tun

        console.log("Fetch-Button wurde geklickt."); // Log-Klick-Ereignis

        // Extrahiere die file_id aus dem data-file-id Attribut des Buttons
        let fileId = button.getAttribute("data-file-id");

        console.log(`Extrahierte File ID: ${fileId}`); // Log-Datei-ID

        if (!fileId) {
            console.error("File ID not found!");
            document.getElementById("error-message").innerText = "Error: File ID not found!";
            return;
        }

        // Optionale: Leere die Fehlernachricht und Vorschau, wenn sie existieren
        document.getElementById("error-message").innerText = "";
        document.getElementById("file-preview").innerHTML = "";

        console.log(`Sende Fetch-Request an /modules/file_search/get/${fileId}`); // Log-Request-Start

        // Fetch-Request an das Flask-Backend, um die Datei zu erhalten
        fetch(`/modules/file_search/get/${fileId}`)
            .then(response => {
                console.log(`Response-Status: ${response.status}`); // Log-HTTP-Statuscode

                if (!response.ok) {
                    throw new Error(`Failed to fetch file: ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                console.log("Daten erfolgreich empfangen:", data); // Log-Empfangene Daten

                if (!data.success) {
                    throw new Error(data.error || "Unknown error");
                }

                // Datei-Rendering durchführen
                const fileContent = data.file_content;
                const fileType = data.file_type;

                console.log(`Render-Datei: Type=${fileType}, Content-Length=${fileContent.length}`);
                renderFile(fileContent, fileType);
            })
            .catch(error => {
                console.error("Fehler beim Abrufen der Datei:", error); // Log-Fehlermeldung
                document.getElementById("preview-card").style.backgroundColor = "black"; // Setze Hintergrundfarbe auf Schwarz
                document.getElementById("file-preview").innerHTML = `
                    <img height="300" src="../../static/img/ERRORS/404.png" alt="Error">
                `; // Leere die Vorschau
                document.getElementById("error-message").style.marginTop = "10px";
                document.getElementById("error-message").innerText = `It seems Poseidon has swept this page away with the tides - or it has been deleted.`;
            });
    });
});