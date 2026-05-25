async def test_deve_tornar_pedido_prioritario(client):
    await client.post("/clientes", json={"cpf": "11111111111", "nome": "Ana"})
    await client.post("/produtos", json={"codigo": 1, "valor": 10.0, "tipo": 2})
    r = await client.post("/lanchonete/pedidos", json={"cpf": "11111111111", "cod_produto": 1, "qtd_max_produtos": 5})
    cod_pedido = r.json()["codigo"]

    response = await client.post(f"/lanchonete/pedidos/{cod_pedido}/prioridade")

    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True


async def test_fila_deve_ter_prioritarios_primeiro(client):
    await client.post("/clientes", json={"cpf": "11111111111", "nome": "Ana"})
    await client.post("/produtos", json={"codigo": 1, "valor": 10.0, "tipo": 2})

    r1 = await client.post("/lanchonete/pedidos", json={"cpf": "11111111111", "cod_produto": 1, "qtd_max_produtos": 5})
    cod_normal = r1.json()["codigo"]

    r2 = await client.post("/lanchonete/pedidos", json={"cpf": "11111111111", "cod_produto": 1, "qtd_max_produtos": 5})
    cod_prioritario = r2.json()["codigo"]
    await client.post(f"/lanchonete/pedidos/{cod_prioritario}/prioridade")

    response = await client.get("/lanchonete/pedidos/fila/preparo")

    assert response.status_code == 200
    fila = response.json()
    assert len(fila) == 2
    assert fila[0]["prioritario"] is True
    assert fila[1]["prioritario"] is False


async def test_fila_nao_deve_listar_cancelados(client):
    await client.post("/clientes", json={"cpf": "11111111111", "nome": "Ana"})
    await client.post("/produtos", json={"codigo": 1, "valor": 10.0, "tipo": 2})

    r = await client.post("/lanchonete/pedidos", json={"cpf": "11111111111", "cod_produto": 1, "qtd_max_produtos": 5})
    cod_pedido = r.json()["codigo"]
    await client.post(f"/lanchonete/pedidos/{cod_pedido}/cancelar")

    response = await client.get("/lanchonete/pedidos/fila/preparo")

    assert response.status_code == 200
    fila = response.json()
    assert all(item["cpf"] != "cancelado" for item in fila)
    assert len(fila) == 0
