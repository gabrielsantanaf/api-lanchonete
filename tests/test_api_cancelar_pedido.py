async def test_deve_cancelar_pedido(client):
    await client.post("/clientes", json={"cpf": "12345678900", "nome": "Joao"})
    await client.post("/produtos", json={"codigo": 1, "valor": 10.0, "tipo": 2})
    r = await client.post("/lanchonete/pedidos", json={"cpf": "12345678900", "cod_produto": 1, "qtd_max_produtos": 5})
    cod_pedido = r.json()["codigo"]

    response = await client.post(f"/lanchonete/pedidos/{cod_pedido}/cancelar")

    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["mensagem"] == "Pedido cancelado com sucesso"


async def test_nao_deve_cancelar_pedido_inexistente(client):
    response = await client.post("/lanchonete/pedidos/999/cancelar")

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Pedido não encontrado ou não pode ser cancelado"


async def test_nao_deve_cancelar_pedido_entregue(client):
    await client.post("/clientes", json={"cpf": "12345678900", "nome": "Joao"})
    await client.post("/produtos", json={"codigo": 1, "valor": 10.0, "tipo": 2})
    r = await client.post("/lanchonete/pedidos", json={"cpf": "12345678900", "cod_produto": 1, "qtd_max_produtos": 5})
    cod_pedido = r.json()["codigo"]
    await client.post(f"/lanchonete/pedidos/{cod_pedido}/finalizar")

    response = await client.post(f"/lanchonete/pedidos/{cod_pedido}/cancelar")

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Pedido não encontrado ou não pode ser cancelado"


async def test_deve_listar_pedidos_cancelados(client):
    await client.post("/clientes", json={"cpf": "12345678900", "nome": "Joao"})
    await client.post("/produtos", json={"codigo": 1, "valor": 10.0, "tipo": 2})
    r = await client.post("/lanchonete/pedidos", json={"cpf": "12345678900", "cod_produto": 1, "qtd_max_produtos": 5})
    cod_pedido = r.json()["codigo"]
    await client.post(f"/lanchonete/pedidos/{cod_pedido}/cancelar")

    response = await client.get("/lanchonete/pedidos/cancelados")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["esta_cancelado"] is True
