async function loadCalculator() {
    const selectedCalculator = document.querySelector('input[name="calculator"]:checked').value;
    const calculatorContainer = document.getElementById('calculator-container');
    const dynamicScripts = document.getElementById('dynamic-scripts');

    // Clear previous content and scripts
    calculatorContainer.innerHTML = '';
    while (dynamicScripts.firstChild) {
        dynamicScripts.removeChild(dynamicScripts.firstChild);
    }

    // Define LOCAL script paths based on selection
    let scriptsToLoad = [];

    if (selectedCalculator === '30year') {
        scriptsToLoad = [
            '../test3/assets/js/modelSwitch.js',
            '../test3/assets/js/plotRisk.js',
            '../test3/assets/js/riskCalculator.js',
            '../test3/assets/js/variableMenu.js'
        ];
    } else if (selectedCalculator === '90day') {
        scriptsToLoad = [
            '../test2/assets/js/modelSwitch.js',
            '../test2/assets/js/plotRisk.js',
            '../test2/assets/js/riskCalculator.js',
            '../test2/assets/js/variableMenu.js'
        ];
    } else {
        scriptsToLoad = [
            '../test4/assets/js/variableMenu.js',
            '../test4/assets/js/riskCalculator.js',
            '../test4/assets/js/plotRisk.js'
        ];
    }

    // Dynamically inject <script> tags
    const loadScripts = scriptsToLoad.map(src => {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = src;
            script.async = false;
            script.onload = () => {
                console.log(`Loaded script: ${src}`);
                resolve();
            };
            script.onerror = () => {
                console.error(`Failed to load script: ${src}`);
                reject(new Error(`Failed to load ${src}`));
            };
            dynamicScripts.appendChild(script);
        });
    });

    // Inject local CSS if not already present
    const cssHref = './assets/css/style.css';
    if (!document.querySelector(`link[href="${cssHref}"]`)) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = cssHref;
        document.head.appendChild(link);
    }

    // Render static calculator HTML
    if (selectedCalculator === '90day') {
        calculatorContainer.innerHTML = `
            <div class="calculator-container">
                <h1>90-Day Mortality Risk Calculator</h1>
                <div class="model-toggle-container">
                    <span id="model1Label">Model 1</span>
                    <label class="switch">
                        <input type="checkbox" id="modelSwitch" onclick="toggleModel()">
                        <span class="slider round"></span>
                    </label>
                    <span id="model2Label">Model 2</span>
                </div>
                <form id="calculator-form">
                    <h2>Set Variables</h2>
                    <div id="variable-inputs"></div>
                    <button type="button" onclick="calculateRisk()">Calculate Risk</button>
                </form>
                <h2>Risk Plot</h2>
                <div id="mortality-risk-graph-container">
                    <div id="mortality-risk-graph"></div>
                </div>
            </div>
        `;
    } else if (selectedCalculator === '30year') {
        calculatorContainer.innerHTML = `
            <div class="calculator-container">
                <h1>30-Year Mortality Risk Calculator</h1>
                <div class="model-toggle-container">
                    <span id="model1Label">Mortality</span>
                    <label class="switch">
                        <input type="checkbox" id="modelSwitch" onclick="toggleModel()">
                        <span class="slider round"></span>
                    </label>
                    <span id="model2Label">ESRD</span>
                </div>
                <form id="calculator-form">
                    <h2>Set Variables For Control Population</h2>
                    <div id="variable-inputs"></div>
                    <h2>Set Variables For Donor Population</h2>
                    <div id="variable-inputs-2"></div>
                    <button type="button" onclick="calculateRisk()">Calculate Risk</button>
                </form>
                <h2>Risk Plot</h2>
                <div id="mortality-risk-graph-container">
                    <div id="mortality-risk-graph"></div>
                </div>
            </div>
        `;
    } else if (selectedCalculator === 'hospitalization') {
        calculatorContainer.innerHTML = `
            <div class="calculator-container">
                <h1>All-cause Hospitalization After Nephrectomy</h1>
                <h1>Among Live Kidney Donors</h1>
                <form id="calculator-form">
                    <h2>Set Variables</h2>
                    <div id="variable-inputs"></div>
                    <button type="button" onclick="calculateRisk()">Calculate Risk</button>
                </form>
                <h2>Risk Plot</h2>
                <div id="hospitalization-risk-graph-container">
                    <div id="hospitalization-risk-graph"></div>
                </div>
            </div>
        `;
    }

    // Wait for all scripts to load, then call model/data functions
    try {
        await Promise.all(loadScripts);

        if (selectedCalculator === '30year' || selectedCalculator === '90day') {
            if (typeof toggleModel === 'function') {
                toggleModel();
            } else {
                console.error('toggleModel() not defined');
            }
        } else {
            if (typeof loadModelData === 'function') await loadModelData();
            if (typeof loadSurvivalData === 'function') await loadSurvivalData();
            if (typeof updateVariableInputs === 'function') updateVariableInputs();
        }
    } catch (err) {
        console.error('Error loading scripts or initializing calculator:', err);
    }
}
# flick 20250409213601-E8RP
# flick 20250409214208-WrsX
# flick 20250409214624-0jdB
# flick 20250409220134-ZymH
# flick 20250409231150-frjT
# flick 20250410002732-tY7A
# flick 20250410003324-gRcf
# flick 20250410004048-t3JI
# flick 20250410014856-3NYp
# flick 20250410030139-lE7S
# flick 20250410031044-t77u
# flick 20250410032005-CLz0
# flick 20250410140618-BVI7
# flick 20250410145600-oLr2
# flick 20250410152045-2nxH
# flick 20250410152850-TEF8
# flick 20250410161627-2kJG
# flick 20250410202641-ZTDN
# flick 20250410205356-SFwu
# flick 20250410213331-rjKY
# flick 20250410235824-Ywiq
# flick 20250413005500-W0LG
# flick 20250413010201-X4Sl
# flick 20250413011053-xlq3
# flick 20250413011338-1Qhq
# flick 20250413233323-WKWw
# flick 20250414004212-gjaF
# flick 20250415192653-Ei1E
# flick 20250415194337-OG6l
# flick 20250415204933-U0uf
# flick 20250415211838-vA8l
# flick 20250416014327-Pjyw
# flick 20250416031040-ECgK
# flick 20250416161509-OJJK
# flick 20250416214705-Sf99
# flick 20250416215309-6YWu
# flick 20250416223139-cWvv
# flick 20250416225807-n5OT
# flick 20250417001511-sB9f
# flick 20250417034855-rQLx
# flick 20250417185032-Bdko
# flick 20250417193143-hU2t
# flick 20250417215302-5Ksu
# flick 20250418022424-UwM1
# flick 20250418022524-yLYR
# flick 20250418040652-aOEf
# flick 20250422032350-wDuH
# flick 20250422235230-XG0n
# flick 20250423014100-R4vm
# flick 20250423021931-uxDT
# flick 20250423180021-P5No
# flick 20250423194208-CIT0
# flick 20250423200222-qZWf
