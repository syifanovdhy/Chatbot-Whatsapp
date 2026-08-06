async function loadConsultations(){

    const response = await fetch(

        "/dashboard/consultations"

    );

    const data = await response.json();

    console.log(data);

}

loadConsultations();