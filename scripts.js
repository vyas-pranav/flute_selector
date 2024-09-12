// scripts.js
const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
const good_bad_code = [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1];
const intervalMap = {
    "S": 0,  "r": 1,  "R": 2,  "g": 3,  "G": 4,
    "m": 5,  "M": 6,  "P": 7,
    "d": 8, "D": 9, "n": 10, "N": 11
};
const indian_notes = ['S', 'r', 'R', 'g', 'G', 'm', 'M', 'P', 'd', 'D', 'n', 'N'];

document.getElementById('calculate-btn').addEventListener('click', () => {
    const scaleInput = document.getElementById('scale-input').value.split(' ');
    const basePitch = document.getElementById('base-pitch-input').value.trim();

    if (!validateInputs(scaleInput, basePitch)) return;

    const basePitchIndex = notes.indexOf(basePitch);
    const westernScalePitches = hindustaniToWestern(scaleInput, basePitchIndex);

    // Display the scale notes in Western notation based on the selected base pitch
    displayWesternScale(westernScalePitches, basePitch);

    const results = evaluateAllPitches(westernScalePitches, basePitchIndex);
    displayPlots(results, basePitchIndex, scaleInput);
});

function validateInputs(scaleInput, basePitch) {
    const validNotes = Object.keys(intervalMap);
    for (let note of scaleInput) {
        if (!validNotes.includes(note)) {
            alert(`Invalid note: ${note}`);
            return false;
        }
    }

    if (!notes.includes(basePitch)) {
        alert('Invalid base pitch. Please choose from: ' + notes.join(', '));
        return false;
    }
    return true;
}

function hindustaniToWestern(scaleNotes, basePitchIndex) {
    return scaleNotes.map(note => (basePitchIndex + intervalMap[note]) % 12);
}

function evaluatePitch(pitchIndex, westernScalePitches) {
    const chromaticScale = Array(12).fill(0);
    westernScalePitches.forEach(pitch => chromaticScale[(pitchIndex + pitch) % 12] = 1);
    
    const resultArray = chromaticScale.map((val, i) => val * good_bad_code[i]);
    return { score: resultArray.reduce((a, b) => a + b, 0), binarySeries: chromaticScale };
}

function evaluateAllPitches(westernScalePitches, basePitchIndex) {
    return notes.map((pitch, i) => {
        const evaluation = evaluatePitch(i, westernScalePitches);
        const saMeans = calculateSaMeans(i, basePitchIndex);
        return { pitch, ...evaluation, saMeans };
    }).sort((a, b) => b.score - a.score);
}

function calculateSaMeans(pitchIndex, basePitchIndex) {
    const shiftedScale = Array(12).fill(0).map((_, i) => (pitchIndex + i) % 12);
    const saIndex = shiftedScale.indexOf(basePitchIndex);
    
    // Find the Indian note for the corresponding Sa index
    for (const [key, value] of Object.entries(intervalMap)) {
        if (value === saIndex) return key;
    }
}

function displayWesternScale(westernScalePitches, basePitch) {
    const westernScaleDiv = document.getElementById('western-scale');
    westernScaleDiv.textContent = `Scale notes in Western notation based on ${basePitch}: ${westernScalePitches.map(pitch => notes[pitch]).join(', ')}`;
}

function displayPlots(results, basePitchIndex, hindustaniScale) {
    const plotContainer = document.getElementById('plot-container');
    plotContainer.innerHTML = ''; // Clear previous plots

    results.forEach(result => {
        const plotElement = document.createElement('div');
        plotElement.classList.add('plot');

        const title = document.createElement('h3');
        title.textContent = `Instrument base pitch: ${result.pitch} (Score: ${result.score})`;
        plotElement.appendChild(title);

        // Add some text to show the Indian notation and Sa means
        const indianNotation = document.createElement('p');
        indianNotation.textContent = `Raga's S = ${result.saMeans} on instrument`;
        plotElement.appendChild(indianNotation);

        // Create two separate canvases for Indian notes and Western pitches
        const canvasIndian = document.createElement('canvas');
        canvasIndian.width = 600;
        canvasIndian.height = 50;
        plotElement.appendChild(canvasIndian);

        const canvasWestern = document.createElement('canvas');
        canvasWestern.width = 600;
        canvasWestern.height = 50;
        plotElement.appendChild(canvasWestern);

        // Get two separate contexts for the two canvases
        const ctxIndian = canvasIndian.getContext('2d');
        const ctxWestern = canvasWestern.getContext('2d');

        // Draw the plots
        drawPlot(ctxIndian, result.binarySeries, result.pitch);  // For Indian notes
        drawPlot1(ctxWestern, result.binarySeries, result.pitch); // For Western pitches

        plotContainer.appendChild(plotElement);
    });
}

function drawPlot(ctx, binarySeries, pitch) {
    const cellWidth = 50;
    const cellHeight = 50;

    binarySeries.forEach((val, i) => {
        ctx.fillStyle = val ? 'orange' : 'white';
        ctx.fillRect(i * cellWidth, 0, cellWidth, cellHeight);
        ctx.strokeRect(i * cellWidth, 0, cellWidth, cellHeight);

        ctx.fillStyle = 'black';
        // Fill text in the middle of the cell with Indian notes in the center of the cell
        ctx.font = 'bold 12px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(indian_notes[i], i * cellWidth + cellWidth / 2, cellHeight / 2);
    });
}

function drawPlot1(ctx, binarySeries, pitch) {
    const cellWidth = 50;
    const cellHeight = 50;

    binarySeries.forEach((val, i) => {
        ctx.fillStyle = val ? 'orange' : 'white';
        ctx.fillRect(i * cellWidth, 0, cellWidth, cellHeight);
        ctx.strokeRect(i * cellWidth, 0, cellWidth, cellHeight);

        ctx.fillStyle = 'black';
        // Fill text in the middle of the cell with the shifted chromatic scale in the center of the cell
        ctx.font = 'bold 12px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(notes[(notes.indexOf(pitch) + i) % 12], i * cellWidth + cellWidth / 2, cellHeight / 2);
    });
}
