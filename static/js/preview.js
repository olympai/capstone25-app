// Funktion zum Rendern von Dateien basierend auf ihrem Typ
export function renderFile(fileContent, fileExtension, offcanvas='preview_offcanvas_body', filePreview='file-preview', errorMessage='error-message') {
    const previewElement = document.getElementById(filePreview);
    const offcanvasElement = document.getElementById(offcanvas);
    
    // Leere vorherigen Inhalt
    previewElement.innerHTML = '';
    offcanvasElement.innerHTML = '';

    switch (fileExtension.toLowerCase()) {
        case 'txt':
            const title = document.createElement('p');
            title.classList.add('voice_heading');
            title.textContent = 'Transcript';
            offcanvasElement.appendChild(title);
            const textSpan = document.createElement('span');
            textSpan.textContent = fileContent;
            previewElement.classList.add('voice_preview');
            previewElement.appendChild(textSpan);
            break;

        case 'pdf':
            const iframePdf = document.createElement('iframe');
            iframePdf.src = `data:application/pdf;base64,${fileContent}`;
            iframePdf.width = '800px';
            iframePdf.height = '700px';
            previewElement.appendChild(iframePdf);
            break;

        case 'jpg':
        case 'jpeg':
        case 'png':
        case 'gif':
            const img = document.createElement('img');
            img.src = `data:image/${fileExtension};base64,${fileContent}`;
            img.alt = 'Image preview';
            img.style.maxWidth = '100%';
            img.style.maxHeight = '600px';
            previewElement.appendChild(img);
            break;

        case 'js':
        case 'php':
        case 'html':
        case 'css':
            const preCode = document.createElement('pre');
            const code = document.createElement('code');
            code.textContent = fileContent;
            preCode.appendChild(code);
            previewElement.appendChild(preCode);
            break;

        case 'xlsx':
        case 'json':
            try {
                console.log(fileContent);
                const data = JSON.parse(fileContent);
                if (Array.isArray(data) && data.length && typeof data[0] === 'object') {
                    const table = document.createElement('table');
                    table.style.width = '100%';
                    table.style.borderCollapse = 'collapse';
                    table.style.marginTop = '10px';
                    
                    const thead = document.createElement('thead');
                    const headerRow = document.createElement('tr');

                    Object.keys(data[0]).forEach(key => {
                        const th = document.createElement('th');
                        th.textContent = key;
                        th.style.border = '1px solid #ccc';
                        th.style.padding = '8px';
                        th.style.backgroundColor = '#2E4057';
                        headerRow.appendChild(th);
                    });
                    thead.appendChild(headerRow);
                    table.appendChild(thead);

                    const tbody = document.createElement('tbody');
                    data.forEach(row => {
                        const tr = document.createElement('tr');
                        Object.values(row).forEach(value => {
                            const td = document.createElement('td');
                            td.textContent = value;
                            td.style.border = '1px solid #ddd';
                            td.style.padding = '6px';
                            tr.appendChild(td);
                        });
                        tbody.appendChild(tr);
                    });
                    table.appendChild(tbody);
                    previewElement.appendChild(table);
                } else {
                    const pre = document.createElement('pre');
                    pre.textContent = JSON.stringify(data, null, 2);
                    previewElement.appendChild(pre);
                }
            } catch (e) {
                console.error("Fehler beim Parsen der JSON-Daten:", e);
                document.getElementById(errorMessage).innerText = "Invalid JSON file.";
            }
            break;

        case 'docx':
            convertDocxToHtml(fileContent, previewElement, offcanvasElement);
            break;

        default:
            document.getElementById(errorMessage).innerText = "This file format cannot be displayed yet.";
            break;
    }
}

// Funktion zur Konvertierung von DOCX in HTML
function convertDocxToHtml(base64Content, previewElement, offcanvasElement) {
    const byteArray = Uint8Array.from(atob(base64Content), c => c.charCodeAt(0));
    const blob = new Blob([byteArray], { type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document" });

    const reader = new FileReader();
    reader.onload = function(event) {
        const arrayBuffer = event.target.result;

        mammoth.convertToHtml({ arrayBuffer: arrayBuffer })
            .then(function(result) {
                const title = document.createElement('p');
                title.classList.add('voice_heading');
                title.textContent = 'Word Preview';
                offcanvasElement.appendChild(title);
                const textSpan = document.createElement('span');
                textSpan.innerHTML = result.value;  // HTML aus DOCX setzen
                previewElement.classList.add('voice_preview');
                previewElement.appendChild(textSpan);
                })
            .catch(function(err) {
                console.error("Fehler beim Konvertieren von DOCX:", err);
                previewElement.innerHTML = "<p>Fehler beim Anzeigen des Word-Dokuments.</p>";
            });
    };

    reader.readAsArrayBuffer(blob);
}