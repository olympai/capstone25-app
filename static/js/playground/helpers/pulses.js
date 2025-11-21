function checkCustomAnimation(link) {
    // custom animation
    let animation_link = link;
    var custom_animation = $('#custom_animation').val();
    if (custom_animation != 'False') {
        animation_link = custom_animation;
    }
    return animation_link;
}

function showPulseAnimation(element) {
    element.innerHTML = `
        <dotlottie-player 
            src="${checkCustomAnimation('https://lottie.host/4564fb01-837e-41a9-bcb5-5320925d9c3e/1TKqGBRcww.lottie')}" 
            background="transparent" 
            speed="1" 
            style="width: 300px; height: 300px" 
            loop 
            autoplay>
        </dotlottie-player>
    `;
    console.log('Pulse animation added');
}

function showQueryingDatabaseAnimation(element) {
    element.innerHTML = `
        <dotlottie-player
            src="${checkCustomAnimation('https://lottie.host/30363484-4a8f-4e99-a12a-ce7a136e804e/U9JEIBV8a8.lottie')}" 
            background="transparent"
            speed="2"
            style="width: 300px; height: 300px"
            loop
            autoplay
        ></dotlottie-player>
    `;
}

function showUsingToolsAnimation(element) {
    element.innerHTML = `
        <dotlottie-player
            src="${checkCustomAnimation('https://lottie.host/2a6b789b-bb30-4ce8-8965-005bc6854800/VLpGlZ9DF5.lottie')}" 
            background="transparent"
            speed="1"
            style="width: 300px; height: 300px"
            loop
            autoplay
        ></dotlottie-player>
    `;
}

function showGeneratingChartAnimation(element) {
    element.innerHTML = `
        <dotlottie-player
            src="${checkCustomAnimation('https://lottie.host/92862762-d0dc-4d2e-9c9f-690f1e81bbe6/UHKg20aki0.lottie')}"
            background="transparent"
            speed="1"
            style="width: 300px; height: 300px"
            loop
            autoplay
        ></dotlottie-player>
    `;
}

function showWebSearchAnimation(element) {
    element.innerHTML = `
        <dotlottie-player
            src="${checkCustomAnimation('https://lottie.host/e0598c8a-29f3-460f-8dde-dcfba77d10e8/ZQhi8xpi0A.lottie')}"
            background="transparent"
            speed="1"
            style="width: 300px; height: 300px"
            loop
            autoplay
        ></dotlottie-player>
    `;
}

function showMailAnimation(element) {
    element.innerHTML = `
        <dotlottie-player
            src="${checkCustomAnimation('https://lottie.host/0b06f038-71d5-47f6-83f5-9f1f87a60ac1/R80n6GAzpi.lottie')}"
            background="transparent"
            speed="1"
            style="width: 300px; height: 300px"
            loop
            autoplay
        ></dotlottie-player>
    `;
}

function showWorkflowAnimation(element) {
    element.innerHTML = `
        <dotlottie-player
            src="${checkCustomAnimation('https://lottie.host/b777e3dc-becf-4c5b-99c0-0dfecb4dc30d/SaoQYL7Ytl.lottie')}"
            background="transparent"
            speed="1"
            style="width: 300px; height: 300px"
            loop
            autoplay
        ></dotlottie-player>
    `;
}

function showThinkingAnimation(element) {
    element.innerHTML = `
        <dotlottie-player
            src="${checkCustomAnimation('https://lottie.host/85a2b4c8-e5b5-4c8b-a8c7-d4b3c2a1b6c5/ThinkingAnimation.lottie')}"
            background="transparent"
            speed="1.5"
            style="width: 300px; height: 300px"
            loop
            autoplay
        ></dotlottie-player>
    `;
}

function showAPIProcessingAnimation(element) {
    element.innerHTML = `
        <dotlottie-player
            src="${checkCustomAnimation('https://lottie.host/f3c5d7e9-a1b2-4c5d-8e7f-9a8b7c6d5e4f/APIProcessing.lottie')}"
            background="transparent"
            speed="2"
            style="width: 300px; height: 300px"
            loop
            autoplay
        ></dotlottie-player>
    `;
}

async function summarizeText(text) {
    try {
        const response = await fetch('/api/summarize_reasoning', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                max_length: 200
            })
        });

        if (response.ok) {
            const data = await response.json();
            return data.summary || 'Thinking ...';
        }
    } catch (error) {
        console.log('Summarization failed, using original text:', error);
    }
    return 'Analyzing ...';
}

function showTextPulse(element, text) {
    if (text.trim() == 'null') {
        text = "Thinking...";
    }

    // Show initial text immediately
    const updateElement = (displayText) => {
        element.innerHTML = `
            <div class="pulse-text-container">
                <div class="pulse-text-header">Reasoning</div>
                <span class="pulse-text">${displayText}</span>
            </div>
        `;
    };
    updateElement(text);
}

function handlePulseAnimation(element, content) {
    const animationMap = {
        // Only non-API animations
        'querying_database': () => showQueryingDatabaseAnimation(element),
        'using_tools': () => showUsingToolsAnimation(element),
        'generating_chart': () => showGeneratingChartAnimation(element),
        'web_search': () => showWebSearchAnimation(element),
        'writing_email': () => showMailAnimation(element),
        'applying_workflow': () => showWorkflowAnimation(element),
        'fulfill_documents': () => showWorkflowAnimation(element),
    };

    // Check for specific animation matches for non-API content
    const animation = animationMap[content];
    if (animation) {
        animation();
        return;
    }

    // For any other unknown content, show as pulsing text
    showTextPulse(element, content);
}

export {
    showPulseAnimation,
    showQueryingDatabaseAnimation,
    showUsingToolsAnimation,
    showGeneratingChartAnimation,
    showWebSearchAnimation,
    showMailAnimation,
    showWorkflowAnimation,
    showThinkingAnimation,
    showAPIProcessingAnimation,
    showTextPulse,
    handlePulseAnimation
};