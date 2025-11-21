// Import necessary functions
import { handleChartModalClick, workWithCharts } from './charting.js';
import { botMessageTemplate, userMessageTemplate } from './html_templates.js';
import { initializeMessages } from './messages.js';
import * as pulses from './helpers/pulses.js';
import { sendFeedback, sendScore } from './helpers/feedback.js';
import { handleTableModalClick } from './helpers/tables.js';
// import { handleCancelRun} from './helpers/run.js';
import { handleFocusButtonClick } from './helpers/focus.js';
import { example_prompts, loadExamplePrompts, initCharacterCounter } from './helpers/example_prompts.js';
import { handleCustomContextMenu, hideAllMenus } from './helpers/context_menu.js';
import { handleUrlFetch } from './helpers/urls.js';
import { handleProfileToggle } from './helpers/profiling.js';

// sumbmit button
const messageSubmitButton = document.getElementById('message_submit_button');
// const cancelRunButton = document.getElementById('cancel_run_button');

$(document).ready(function () {
    // Translate
    document.addEventListener('click', function (event) {
        const button = event.target.closest('.translate_field');
        if (!button) return; // Klick war nicht auf einem passenden Button
      
        const value = `Translate to`;
        example_prompts(value);
    });

    document.addEventListener("contextmenu", function (e) {
        console.log('Context menu triggered');
        handleCustomContextMenu(e, {
            messageSelector: '.hovering_message',
            menuClass: '.custom-menu',
            menuIdPrefix: 'custom_',
            wrapperIdPrefix: 'menu_'
        });
    });
    
    document.addEventListener("click", function () {
        hideAllMenus('.custom-menu');
    });

    // Tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();

    // Initialize messages
    initializeMessages();

    // URL Offcanvas
    $(document).on('click', '#fetchurl', function (event) {
        const messageId = $(this).attr('data-message-id');
        const urlSpace = document.getElementById('url-space');
        handleUrlFetch(messageId, urlSpace);
    });

    // Profile Action Button
    document.querySelectorAll(".profile_action_button").forEach(button => {
        button.addEventListener("click", () => {
            const profileId = button.id;
            const focusCardElement = button.closest('.focus_card');
            const userMessageElement = document.getElementById('user_message');
            const allProfileCardElements = document.querySelectorAll('.filled_primary.profiling_card');
    
            if (focusCardElement && focusCardElement.classList.contains('focus_card')) {
                handleProfileToggle({
                    profileId,
                    focusCardElement,
                    userMessageElement,
                    allProfileCardElements
                });
            }
        });
    });

    // Chart Export Modal
    const chartModal = $('#chartExportModal');
    $(document).on('click', '#chartModalButton', function (event) {
        console.log('Chart Modal Button clicked');
        handleChartModalClick($(this), chartModal);
    });

    // Table Export Modal
    const tableModal = $('#tablesExportModal');
    $(document).on('click', '#tablesModalButton', function () {
        console.log('Table Modal Button clicked');
        handleTableModalClick($(this), tableModal);
    });

    // cancel run button
    // const abortController = new AbortController();
    // $('#cancel_run_button').on('click', function () {
    //     console.log('Cancelling stream...');
    //     abortController.abort();
    //     handleCancelRun(this);
    // });

    // Focus
    document.querySelectorAll(".focus_action_button").forEach(button => {
        button.addEventListener("click", () => {
            handleFocusButtonClick(button);
        });
    });

    // load example prompts on page load
    window.addEventListener('load', function() {
        loadExamplePrompts();
        initCharacterCounter();
    });

    // click on example prompts button, insert the prompt into the input field
    document.getElementById('example_prompts_field').addEventListener('click', function (event) {
        if (event.target.classList.contains('insertButton')) {
            const value = event.target.value;
            example_prompts(value);
        }
    });

    // Limit input character to 1000
    document.getElementById("user_message").addEventListener("input", function () {
        let maxLength = 200000; // ~50k Tokens für User-Input
        if (this.value.length > maxLength) {
          this.value = this.value.substring(0, maxLength);
        }
    });

    // Character counter for keyword inputs
    document.addEventListener('input', function(e) {
        if (e.target.classList.contains('keyword-input')) {
            const currentLength = e.target.value.length;
            const maxLength = e.target.getAttribute('maxlength') || 50;
            const threadId = e.target.id.replace('new_keyword_', '');
            const charCountElement = document.getElementById(`keyword_char_count_${threadId}`);
            if (charCountElement) {
                charCountElement.textContent = `${currentLength}/${maxLength}`;
            }
        }
    });

    // Event handlers for feedback submission
    $(document).on('click', '#feedback-submit-btn', function (e) {
        e.preventDefault();
        var view_id = $(this).val();
        sendFeedback(view_id, $(`textarea[name="feedback_${view_id}"]`).val());
    });

    // Event handler for score submission
    $(document).on('click', '#score-submit-btn', function (e) {
        e.preventDefault();
        var view_id = $(this).val();
        sendScore(view_id, $(`#stars_${view_id}`).val());
    });

    let typewriterQueue = [];
    let isTyping = false;
    let currentContent = '';
    let isStreamCompleted = false;
    let isPollingActive = false; // Track if polling is active

    // set message counter
    let messageCount = 0;

    // Typewriter function
    function typewriterEffect(element, newText, speed = 20) {
        return new Promise((resolve) => {
            let i = 0;
            const typing = () => {
                if (i < newText.length) {
                    currentContent += newText.charAt(i);

                    element.innerHTML = marked.parse(currentContent);

                    MathJax.typesetPromise([element]).catch(err => console.error(err.message));

                    i++;
                    // Use faster speed if stream is complete
                    const currentSpeed = isStreamCompleted ? Math.max(speed / 4, 5) : speed;
                    setTimeout(typing, currentSpeed);
                } else {
                    resolve();
                }
            };
            typing();
        });
    }

    // Process typewriter queue
    async function processTypewriterQueue() {
        if (isTyping || typewriterQueue.length === 0) return;
        
        isTyping = true;
        
        while (typewriterQueue.length > 0) {
            const { element, text } = typewriterQueue.shift();
            console.log('Processing typewriter queue for element:', element, 'with text:', text);
            await typewriterEffect(element, text);
        }
        
        isTyping = false;
    }

    // submit user message
    $('#chat-form').on("submit", async (e) => {
        e.preventDefault();
        console.log('submit started');
        // prevents reloading the page on submit

        // Prevent submission if polling is active
        if (isPollingActive) {
            console.log('Cannot submit: another message is being processed');
            return;
        }

        // get the user input and the workframe_id (chat_code) or the input from the suggestions
        var userMessage = "";
        if ($('#user_message').val()) {
            userMessage = $('#user_message').val();
        }

        if (!userMessage) {
            console.log('Kein gültigen Benutzer-Input gefunden.');
        }

        // check whether there is a user input
        if (userMessage.trim() !== '') {

            // Set polling as active
            isPollingActive = true;

            // hide the message submit button
            messageSubmitButton.style.display = 'none';

            var ThreadId = $('#current_thread_id').val();

            messageCount++; // Erhöhe den Zähler für jede Nachricht

            // append the user message
            $('#messages').append(userMessageTemplate(userMessage));

            // delete focus
            document.querySelectorAll('.focus_card.filled_primary:not(.profiling_card)').forEach(el => {
                el.classList.remove('filled_primary');
            });            

            // clear user input field
            $('#user_message').val('');

            // Append a unique bot message container with a unique ID
            const botMessageId = `bot_message_${messageCount}`; // Eindeutige ID fuer jede Nachricht (nur Text)
            const wholebotMessageId = `wholebotmessage_${messageCount}`; // Eindeutige ID fuer jeden Nachrichten Chunk (Text und Charts)
            const sqlMessageId = `sql_message_${messageCount}`; // Eindeutige ID fuer den SQL-Textbereich
            const actionMessageId = `action_message_${messageCount}`;

            // Append bot message dynamically
            const botMessageHtml = botMessageTemplate(wholebotMessageId, botMessageId, sqlMessageId, actionMessageId, messageCount);
            $('#messages').append(botMessageHtml);

            // create empty message
            const MessageField = document.getElementById(botMessageId);

            // append loader
            pulses.showPulseAnimation(MessageField);
            console.log('Pulse text added');

            // scroll to bottom
            window.scrollTo(0, document.body.scrollHeight);

            // Call the async message streaming function here
            try {
                await startStream();
            } catch (e) {
                console.error("Loading Error: ", e);

                // Reset polling flag on error
                isPollingActive = false;
                messageSubmitButton.style.display = 'block';

                if (e instanceof TypeError && e.message === 'Load failed') {
                    // Save content on timeout
                    $.ajax({
                        url: "/playground/save_content_timeout",
                        method: 'POST',
                        contentType: 'application/json',
                        data: JSON.stringify({ thread_id: ThreadId, content: MessageField.textContent }),
                        success: function (response) {
                            console.log(response);
                            console.log('Save content for timeout successful');
                            MessageField.insertAdjacentHTML('beforeend', `<div class="alert alert-warning" role="alert">Timeout: To save resources, the message was cut here.</div>`);
                        },
                        error: function (error) {
                            console.error('Error saving content on timeout:', error);
                            MessageField.insertAdjacentHTML(
                                'beforeend',
                                '<div class="alert alert-danger" role="alert">An error occurred while saving the content. Please try again later!</div>'
                            );
                        }
                    });
                } else {
                    MessageField.insertAdjacentHTML(
                        'beforeend',
                        '<div class="alert alert-danger" role="alert">An error occurred. Most likely, due to a timeout. Please try again later!</div>'
                      );
                 }
                window.scrollTo(0, document.body.scrollHeight);
            }

            async function startStream() {
                console.log('Start Stream called');
                const res = await fetch("/playground/start-stream", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ user_message: userMessage, thread_id: ThreadId })
                });
                
                if (!res.ok) {
                    throw new Error(`HTTP error! status: ${res.status}`);
                }
                
                const { task_id } = await res.json();
                console.log('Task ID received:', task_id);
                
                // Sofort mit dem Polling beginnen, ohne Verzögerung
                await pollStreamMessages(task_id);
            }

            // Optimierte asynchrone message streaming function
            async function pollStreamMessages(taskId) {
                console.log('Poll stream started for task:', taskId);

                // new abort controller
                // const abortController = new AbortController();
                // const signal = abortController.signal;

                let lastText = "";
                let buffer = "";
                let pollAttempts = 0;
                const maxPollAttempts = 2000; // 5 Minuten bei 1s Intervall
                let isStreamComplete = false;

                // Reset stream completion flag at start of new message
                isStreamCompleted = false;

                while (!isStreamComplete && pollAttempts < maxPollAttempts) {
                    pollAttempts++;

                    // Prüfe ob abgebrochen wurde
                    // if (signal.aborted) {
                    //     console.log('Stream wurde abgebrochen');
                        
                    //     // Cleanup
                    //     typewriterQueue = [];
                    //     isTyping = false;
                    //     currentContent = '';

                    //     break;
                    // }
                    
                    try {
                        const response = await fetch(`/playground/get-stream/${taskId}`);
                        
                        if (!response.ok) {
                            console.error('Stream fetch error:', response.status, response.statusText);
                            await new Promise(r => setTimeout(r, 1000));
                            continue;
                        }
                        
                        const data = await response.json();
                        const { text, done } = data;
                        
                        console.log('Poll attempt:', pollAttempts, 'Done:', done, 'Text length:', text?.length || 0);
                        
                        // Auch wenn text leer ist, aber done=true, müssen wir weitermachen
                        if (text && text.length > lastText.length) {
                            const newText = text.slice(lastText.length);
                            lastText = text;
                            buffer += newText;
                            console.log('New text chunk received, buffer length:', buffer.length);
                        }
                        
                        // Buffer verarbeiten, auch wenn kein neuer Text da ist
                        if (buffer) {
                            buffer = await processBuffer(buffer, taskId);
                        }
                        
                        // Stream als komplett markieren wenn done=true
                        if (done) {
                            console.log('Stream marked as complete');
                            isStreamComplete = true;

                            // Set global flag to speed up typewriter effect
                            isStreamCompleted = true;
                            console.log('Typewriter speed increased - stream completed');

                            // Finalen Buffer verarbeiten
                            if (buffer) {
                                await processFinalBuffer(buffer, taskId);
                            }
                        }
                        
                    } catch (error) {
                        console.error('Error in poll stream:', error);
                        await new Promise(r => setTimeout(r, 600));
                        continue;
                    }
                    
                    // Kurze Pause zwischen Polling-Requests
                    if (!isStreamComplete) {
                        await new Promise(resolve => setTimeout(resolve, 200)); // Reduziert auf 200ms für schnellere Reaktion
                    }
                }
                
                if (pollAttempts >= maxPollAttempts) {
                    console.error('Max poll attempts reached');
                    MessageField.insertAdjacentHTML(
                        'beforeend',
                        '<div class="alert alert-warning" role="alert">Stream timeout reached. Please try again.</div>'
                    );
                }
                
                // Cleanup
                await finalizeStream();
            }

            // Buffer verarbeiten und unvollständige Teile zurückgeben
            async function processBuffer(buffer, taskId) {
                if (!buffer.trim()) return '';
                
                const parts = buffer.split(/(?=data:)/);
                let remainingBuffer = '';
                
                // Alle vollständigen Teile verarbeiten (außer dem letzten)
                for (let i = 0; i < parts.length - 1; i++) {
                    if (parts[i].trim()) {
                        await processDataChunk(parts[i], taskId);
                    }
                }
                
                // Letzten Teil prüfen - könnte unvollständig sein
                const lastPart = parts[parts.length - 1];
                if (lastPart && lastPart.trim()) {
                    try {
                        // Versuchen zu parsen
                        const cleaned = lastPart.replace(/^data:/, '').trim();
                        JSON.parse(cleaned);
                        // Wenn erfolgreich, verarbeiten
                        await processDataChunk(lastPart, taskId);
                    } catch (e) {
                        // Wenn parsing fehlschlägt, im Buffer behalten
                        remainingBuffer = lastPart;
                    }
                }
                
                return remainingBuffer;
            }

            // Finalen Buffer verarbeiten (am Ende des Streams)
            async function processFinalBuffer(buffer, taskId) {
                if (!buffer.trim()) return;
                
                const parts = buffer.split(/(?=data:)/);
                
                for (const part of parts) {
                    if (part.trim()) {
                        try {
                            await processDataChunk(part, taskId);
                        } catch (e) {
                            console.error('Error processing final buffer part:', e);
                        }
                    }
                }
            }

            // Einzelnen Data-Chunk verarbeiten
            async function processDataChunk(chunk, taskId) {
                try {
                    const cleanedChunk = chunk.replace(/^data:/, '').trim();
                    if (!cleanedChunk) return;
                    
                    const parsedData = JSON.parse(cleanedChunk);
                    console.log('Processing chunk:', parsedData.type, parsedData);
                    
                    // Cancel button setup
                    // if (parsedData.message_id && parsedData.run_id) {
                    //     cancelRunButton.setAttribute("data-message-id", parsedData.message_id);
                    //     cancelRunButton.setAttribute("data-run-id", parsedData.run_id);
                    //     cancelRunButton.setAttribute("data-task-id", taskId);
                    //     cancelRunButton.style.display = 'block';
                    // }
                    
                    // Pulse animations
                    if (parsedData.type === 'pulse') {
                        handlePulseAnimation(parsedData.content);
                    }
                    
                    // Message content
                    if (parsedData.type === 'message') {
                        await handleMessageContent(parsedData);
                    }
                    
                    // Warnings
                    if (parsedData.type === 'warning') {
                        MessageField.insertAdjacentHTML('beforeend', 
                            `<div class="alert alert-warning" role="alert">${parsedData.content}</div>`
                        );
                    }
                    
                    // Charts
                    if (parsedData.type === 'charts') {
                        handleChartsData(parsedData);
                    }
                    
                } catch (error) {
                    console.error('Error processing data chunk:', error, 'Chunk:', chunk);
                }
            }

            // Pulse Animation Handler
            function handlePulseAnimation(content) {
                pulses.handlePulseAnimation(MessageField, content);
            }

            // Message Content Handler
            async function handleMessageContent(parsedData) {
                let newOutput = parsedData.content.replace('【functions†source】', '').replace(/\[/g, '\\[').replace(/\]/g, '\\]');

                let lastAnnotation = null;

                // Annotations verarbeiten
                if (parsedData.anno && Array.isArray(parsedData.anno)) {
                    parsedData.anno.forEach(annotation => {
                        const regex = new RegExp(annotation.annotation_text, "g");
                        newOutput = newOutput.replace(regex, (match, offset, string) => {
                            if (
                                lastAnnotation === annotation.annotation_index &&
                                string.substring(offset - lastAnnotation.length, offset) === lastAnnotation
                            ) {
                                return match;
                            } else {
                                lastAnnotation = annotation.annotation_index;
                                return annotation.annotation_index;
                            }
                        });
                    });
                }

                // Zu Typewriter Queue hinzufügen
                if (newOutput) {
                    typewriterQueue.push({
                        element: MessageField,
                        text: newOutput
                    });
                    
                    // Queue abarbeiten
                    processTypewriterQueue();
                }
            }

            // Charts Handler
            function handleChartsData(parsedData) {
                console.log('Processing charts data');
                workWithCharts({
                    wholebotMessageIdField: document.getElementById(wholebotMessageId),
                    sqlMessageIdField: document.getElementById(sqlMessageId),
                    actionMessageIdField: document.getElementById(actionMessageId),
                    appendixField: document.getElementById(`custom_${messageCount}`),
                    messageField: document.getElementById(wholebotMessageId),
                    parsedData: parsedData,
                    modalsContainer: document.getElementById('modals'),
                    messageId: parsedData.message_id,
                });
            }

            // Stream finalisieren
            async function finalizeStream() {
                console.log('Finalizing stream');

                // Auf Typewriter-Queue warten
                while (isTyping || typewriterQueue.length > 0) {
                    await new Promise(resolve => setTimeout(resolve, 100));
                }

                // Base64 Bilder durch Fehlermeldung ersetzen
                if (MessageField.innerHTML.includes("data:image/png;base64")) {
                    console.warn("Detected base64 image, replacing content with a generic message.");
                    MessageField.innerHTML = `
                        I tried to generate a chart for you. If an error occurred, please try again later!
                    `;
                }

                // Cleanup
                typewriterQueue = [];
                isStreamCompleted = false; // Reset for next message
                isTyping = false;
                currentContent = '';

                // Reset polling flag
                isPollingActive = false;

                // UI zurücksetzen
                // cancelRunButton.style.display = 'none';
                messageSubmitButton.style.display = 'block';

                console.log('Stream finalized');
            }
        }
    });
});