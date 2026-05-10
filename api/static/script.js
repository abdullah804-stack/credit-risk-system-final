document.getElementById("loanForm").addEventListener("submit", async function (e) {

    e.preventDefault();

    const resultDiv = document.getElementById("result");

    resultDiv.innerHTML = `
        <div class="loading">
            Predicting Risk...
        </div>
    `;

    const data = {

        loan_amnt: parseFloat(document.getElementById("loan_amnt").value),

        term: document.getElementById("term").value,

        int_rate: parseFloat(document.getElementById("int_rate").value),

        installment: parseFloat(document.getElementById("installment").value),

        annual_inc: parseFloat(document.getElementById("annual_inc").value),

        dti: parseFloat(document.getElementById("dti").value),

        open_acc: 15,
        pub_rec: 2,
        revol_bal: 40000,
        revol_util: 92,
        total_acc: 18,
        mort_acc: 0,
        pub_rec_bankruptcies: 1
    };

    console.log("Sending Data:", data);

    try {

        const response = await fetch("/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)
        });

        const result = await response.json();

        console.log(result);

        let riskClass = result.prediction === 1
            ? "risk-high"
            : "risk-low";

        let riskText = result.prediction === 1
            ? "High Risk"
            : "Low Risk";

        resultDiv.innerHTML = `

            <div class="result-box">

                <h2 class="${riskClass}">
                    ${riskText}
                </h2>

                <div class="probability">
                    Default Probability:
                    <strong>
                        ${(result.probability * 100).toFixed(2)}%
                    </strong>
                </div>

            </div>
        `;

    } catch (error) {

        console.error(error);

        resultDiv.innerHTML = `

            <div class="result-box">

                <h2 class="risk-high">
                    Prediction Failed
                </h2>

            </div>
        `;
    }
});