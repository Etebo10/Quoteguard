const form =
    document.getElementById("quote-form");

const button =
    document.getElementById("analyze-button");

const results =
    document.getElementById("results");

const errorBox =
    document.getElementById("error");


function money(value) {

    return new Intl.NumberFormat(
        "en-NG",
        {
            style: "currency",
            currency: "NGN",
            maximumFractionDigits: 2
        }
    ).format(value);

}


function percentage(value) {

    return `${(
        value * 100
    ).toFixed(1)}%`;

}


form.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();


        errorBox.classList.add("hidden");

        results.classList.add("hidden");

        button.disabled = true;

        button.textContent =
            "Analyzing quote...";


        try {

            const payload = {
    customer_name:
        document.getElementById(
            "customer_name"
        ).value,

    customer_email:
        document.getElementById(
            "customer_email"
        ).value,

    project_name:
        document.getElementById(
            "project_name"
        ).value,

    service_type:
        document.getElementById(
            "service_type"
        ).value,

                labor_hours:
                    Number(
                        document.getElementById(
                            "labor_hours"
                        ).value
                    ),

                labor_rate:
                    Number(
                        document.getElementById(
                            "labor_rate"
                        ).value
                    ),

                material_cost:
                    Number(
                        document.getElementById(
                            "material_cost"
                        ).value
                    ),

                overhead_rate:
                    Number(
                        document.getElementById(
                            "overhead_rate"
                        ).value
                    ) / 100,

                contingency_rate:
                    Number(
                        document.getElementById(
                            "contingency_rate"
                        ).value
                    ) / 100,

                target_margin:
                    Number(
                        document.getElementById(
                            "target_margin"
                        ).value
                    ) / 100,

                historical_estimation_variance:
                    0

            };


            const response =
                await fetch(
                    "/intelligence/analyze",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                payload
                            )
                    }
                );


            const responseText = await response.text();
            let data = null;

            try {
                data = responseText ? JSON.parse(responseText) : null;
            } catch {
                data = null;
            }

            if (!response.ok) {
                const errorMessage = data?.detail
                    || data?.message
                    || responseText
                    || "Quote analysis failed.";

                throw new Error(errorMessage);
            }

            if (!data) {
                throw new Error("Quote analysis returned an empty response.");
            }


            displayResults(data);


        } catch (error) {

            errorBox.textContent =
                error.message;

            errorBox.classList.remove(
                "hidden"
            );

        } finally {

            button.disabled = false;

            button.textContent =
                "Analyze Quote";

        }

    }
);


function displayResults(data) {

    results.classList.remove(
        "hidden"
    );


    document.getElementById(
        "recommended-price"
    ).textContent =
        money(
            data.recommended_price
        );


    document.getElementById(
        "total-cost"
    ).textContent =
        money(
            data.total_cost
        );


    document.getElementById(
        "expected-profit"
    ).textContent =
        money(
            data.expected_profit
        );


    document.getElementById(
        "expected-margin"
    ).textContent =
        percentage(
            data.expected_margin
        );


    const ai =
        data.ai_analysis;


    if (ai) {

        document.getElementById(
            "decision-summary"
        ).textContent =
            ai.overall_assessment;


        document.getElementById(
            "assessment"
        ).textContent =
            ai.overall_assessment;


        document.getElementById(
            "pricing-assessment"
        ).textContent =
            ai.pricing_assessment;


        document.getElementById(
            "decision"
        ).textContent =
            ai.decision;


        document.getElementById(
            "decision-reason"
        ).textContent =
            ai.decision_reason;


        populateList(
            "concerns",
            ai.key_concerns
        );


        populateList(
            "recommendations",
            ai.recommendations
        );

    }

}


function populateList(
    elementId,
    items
) {

    const element =
        document.getElementById(
            elementId
        );


    element.innerHTML = "";


    items.forEach(
        function(item) {

            const li =
                document.createElement(
                    "li"
                );

            li.textContent = item;

            element.appendChild(li);

        }
    );

}