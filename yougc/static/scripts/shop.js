function buyProduct(server, name, long_name) {
  if (confirm("Вы действительно хотите купить " + long_name + "?")) {
        document.location.href = "/buy/" + server + "/" + name;
    }
}