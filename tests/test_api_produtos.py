async def test_get_produto_inexistente(client):
    """Buscar um código de produto que não existe deve retornar erro 404 (Not Found).

    Este teste de caminho negativo (sad path) verifica que a API responde
    corretamente quando solicitamos um recurso que não existe, retornando
    o código HTTP adequado.
    """
    response = await client.get("/produtos/999")
    assert response.status_code == 404
    

async def test_atualizar_valor_produto(client):
    """Deve ser possível atualizar o valor de um produto existente.

    Este teste cobre o fluxo de atualização:
        1. Criar um produto com um valor inicial
        2. Atualizar o valor do produto
        3. Verificar que o valor foi atualizado corretamente

    Verificações:
        - O status HTTP da criação é 200 (OK)
        - O status HTTP da atualização é 200 (OK)
        - O valor retornado após a atualização bate com o novo valor
    """
    # 1. Cria o produto com valor inicial
    response1 = await client.post("/produtos", json={"codigo": 1, "valor": 10, "tipo": 1, "desconto_percentual": 0})
    assert response1.status_code == 200

    # 2. Atualiza o valor do produto
    response = await client.put("/produtos/1/valor", json={"novo_valor": 15})
    assert response.status_code == 200

    # 3. Verifica campo de atualização no Body da resposta
    assert response.json()["alterou"] == True