function loadScript(url) {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = url;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });
}

function addStyle(href) {
    const link = document.createElement('link');
    link.href = href;
    link.type = "text/css";
    link.rel = "stylesheet";
    document.head.appendChild(link);
}

function requireAsync(urls) {
    return new Promise((resolve, reject) => {
        try {
            window.requirejs(urls, (...args) => {
                resolve(args);
            });
        } catch (e) {
            reject(e);
        }
    });
}

function getWidgetManager(voila, kernel) {
    function connect() {
    }

    return new voila.WidgetManager({
            saveState: { connect },
            sessionContext: {
                session: { kernel },
                kernelChanged: { connect },
                statusChanged: { connect },
                connectionStatusChanged: { connect },
            },
        },
        new voila.RenderMimeRegistry(),
        { saveState: false });
}

async function connectToJupyterKernel(kernelId, baseUrl, targetModelId) {
    await loadScript('https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js');

    const [voila] = await requireAsync([`${baseUrl}voila/static/voila.js`]);
    const kernel = await voila.connectKernel(baseUrl, kernelId);

    const widgetManager = getWidgetManager(voila, kernel);

    await widgetManager._build_models();

    const model = await widgetManager._models[targetModelId]
    const container = document.getElementById('popout-widget-container')
    if (!model) {
        container.innerText = 'Model not found';
        return;
    }
    widgetManager.display_model(
        undefined,
        model,
        { el: container }
    );
}

const urlParams = new URLSearchParams(window.location.search);
const kernelId = urlParams.get('kernelid');
const modelId = urlParams.get('modelid');
const baseUrl = urlParams.get('baseurl');

addStyle(`${baseUrl}voila/static/index.css`);
addStyle(`${baseUrl}voila/static/theme-light.css`);

connectToJupyterKernel(kernelId, baseUrl, modelId);
