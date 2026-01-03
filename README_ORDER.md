# Rotas de Pedidos (Order)

Este documento explica como consumir as rotas relacionadas a pedidos na API.

Base URL (exemplo local): http://localhost:5000

## Endpoints

1) Criar pedido

- Método: POST
- URL: /order/new
- Descrição: Cria um pedido a partir de um carrinho existente.

Request JSON:
{
  "user_id": "<user_public_id>",
  "cart_id": <cart_id>,
  "address_id": <address_id>
}

Resposta (201 - sucesso):
{
  "error": false,
  "message": "Pedido criado com sucesso!",
  "order": {
    "id": ...,
    "user": {...},
    "total_price": 123.45,
    "created_at": "...",
    "phone_number": ".../null",
    "public_id": "...",
    "address_id": ...,
    "status": "Pendente"
  }
}

Erros comuns (400):
- Usuário não encontrado.
- Endereço não encontrado.
- Carrinho não encontrado.
- Carrinho vazio.

Exemplo curl:

curl -X POST http://localhost:5000/order/new \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user_public_id_123","cart_id":1,"address_id":2}'


2) Atualizar status do pedido

- Método: PATCH
- URL: /order/<order_public_id>/status
- Descrição: Atualiza o status do pedido. Os status aceitos são (em português):
  - Pendente
  - Confirmado
  - Entregue
  - Cancelado

Request JSON:
{
  "status": "Confirmado"
}

Resposta (200 - sucesso):
{
  "error": false,
  "message": "Status do pedido atualizado com sucesso!",
  "order": { ... }
}

Erros comuns (400):
- Campo `status` obrigatório.
- Status inválido.
- Pedido não encontrado.

Exemplo curl:

curl -X PATCH http://localhost:5000/order/ORDER_PUBLIC_ID_123/status \
  -H "Content-Type: application/json" \
  -d '{"status":"Confirmado"}'


Notas e observações

- O endpoint de criação usa o `cart_id` (id do modelo Cart) e o `address_id` (id do modelo Address).
- Ao criar o pedido, todos os itens do carrinho são transformados em `OrderItem` e depois removidos do carrinho.
- O campo `phone_number` no pedido é opcional e será preenchido a partir do carrinho quando disponível.
- As respostas seguem o padrão usado pelo projeto: um objeto com `error`, `message` e dados quando aplicável.

Se quiser, posso adicionar exemplos em Postman ou testes unitários que chamem essas rotas automaticamente.
