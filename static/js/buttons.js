function fixInterface(alreadyRunning) {
    console.log('fixInterface: alreadyRunning: ' + alreadyRunning)

    // Adjusting buttons  
    var analysisRunningInput = $('#analysisRunningHidden');
    var setResetButton = $('#setResetButton');
    var stepIntoButton = $('#stepIntoButton');

    // Check the value of the analysisRunningInput
    var isRunning = analysisRunningInput.val() === 'True';

    // Enable or disable the stepIntoButton based on the analysisRunningInput value
    if (alreadyRunning) {
        setResetButton.text('Reiniciar');
        stepIntoButton.prop('disabled', false);
    } else {
        setResetButton.text('Executar');
        stepIntoButton.prop('disabled', true);
    }
};