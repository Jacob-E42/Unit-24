const BASE_URL = "http://localhost:5000/api";
$cupcakes = $('#cupcake-list')



//given a JSON cupcake, return html that displays its attributes
function generateHTML(cupcake) {
    return `<div data-cupcake-id=${cupcake.id}> 
        <li>${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}</li>
        <img src=${cupcake.image}>
    </div>`;
}

//make response to cupcake api, using axios, and append a list of each cupcake to the DOM, using jQuery
async function displayList() {

    const resp = await axios.get(`${BASE_URL}/cupcakes`);
    cupcakes = resp.data.cupcakes
    for (let cupcake of cupcakes) {
        $newCupcake = $(generateHTML(cupcake))
        $cupcakes.append($newCupcake)
    }
}

//Submit post request to api when form is submitted, and use returned json to append new cupcake to DOM
$('#cupcake-form').on("submit", async function (evt) {
    evt.preventDefault()

    let flavor = $('#flavor').val();
    let size = $('#size').val();
    let rating = $('#rating').val();
    let image = $('#image').val();

    const response = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor: flavor,
        size: size,
        rating: rating,
        image: image
    });

    let $newCupcake = $(generateHTML(response.data.cupcake))
    $cupcakes.append($newCupcake)
    $cupcakes.trigger("reset");
});



//jQuery func runs when DOM is finished loading
$(displayList);