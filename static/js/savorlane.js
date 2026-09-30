const fulfillment = document.querySelector('[name="fulfillment"]');
if (fulfillment) {
  const update = () => {
    const delivery = fulfillment.value === 'DELIVERY';
    for (const name of ['address', 'city', 'pincode']) {
      const input = document.querySelector(`[name="${name}"]`);
      if (input) { input.required = delivery; input.closest('.field').hidden = !delivery; }
    }
  };
  fulfillment.addEventListener('change', update); update();
}
