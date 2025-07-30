import asyncio
import pytest
from httpx import ASGITransport, AsyncClient
from src.app import app
from datetime import datetime, timedelta

@pytest.mark.asyncio(loop_scope="session")
async def test_get_all(get_fixture_data, test_lock):
    data = get_fixture_data
    async with test_lock:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as ac:
            response = await ac.get("/trade/all")
            assert response.status_code == 200
            assert len(data) == len(response.json())
    await asyncio.sleep(0.3)

@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize("test_delta_input, expected", [("0", 2), ("1", 4), ("2", 6), ("3", 7)])
async def test_last_trading_days(test_delta_input, expected, test_lock):
    async with test_lock:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as ac:
            response = await ac.get(f"/trade/last_trading_dates?days_delta={test_delta_input}")
            assert response.status_code == 200
            assert len(response.json()) == expected
            await asyncio.sleep(0.3)
  
@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "start_date, end_date, delivery_type_id, delivery_basis_id",
    [   
        (datetime.now().date(), datetime.now().date() - timedelta(days=3), None, None),
        (datetime.now().date() - timedelta(days=3), datetime.now().date(), "A", None),
        (datetime.now().date() - timedelta(days=3), datetime.now().date(), None, "LUL"),
    ],
)
async def test_dynamics(test_lock, start_date, end_date, delivery_type_id, delivery_basis_id):
    ids_for_test_delyvery_type = [28040, 28143, 1165]
    ids_for_test_delivery_basis_id = [1952]
    async with test_lock:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as ac:
            params = {
                "start_date": start_date,
                "end_date": end_date,
                "delivery_type_id": delivery_type_id,
                "delivery_basis_id": delivery_basis_id
            }
            query_params = {k: v for k, v in params.items() if v is not None}           
            response = await ac.get("/trade/dynamics", params=query_params)
            if start_date > end_date:  
                assert response.status_code == 400
            else:
                ids_data_from_response = [item["id"] for item in response.json()]
                if delivery_type_id is not None:
                    assert response.status_code == 200
                    assert len(response.json()) == 3
                    assert all(item_id in ids_for_test_delyvery_type for item_id in ids_data_from_response)
                elif delivery_basis_id is not None:
                    assert response.status_code == 200
                    assert len(response.json()) == 1
                    assert all(item_id in ids_for_test_delivery_basis_id for item_id in ids_data_from_response)                 
        await asyncio.sleep(0.3)

@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "start_date,oil_id, delivery_type_id, delivery_basis_id, expected_number_of_records",
    [
        (datetime.now().date() - timedelta(days=3), "DST5", "O", "VLD", 1),
        (datetime.now().date() - timedelta(days=3), "PPBA", None, None, 2),
        (datetime.now().date() - timedelta(days=3), None, None, None, 7),
    ],
)
async def test_trading_results(test_lock, start_date, oil_id, delivery_type_id, delivery_basis_id, expected_number_of_records):
    async with test_lock:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as ac:
            params = {
                "start_date": start_date,
                "oil_id": oil_id,
                "delivery_type_id": delivery_type_id,
                "delivery_basis_id": delivery_basis_id
            }
            query_params = {k: v for k, v in params.items() if v is not None}
            response = await ac.get("/trade/trading_results", params=query_params)
            print(response.json(), response.status_code)
            assert response.status_code == 200
            assert len(response.json()) == expected_number_of_records
            await asyncio.sleep(0.3)
