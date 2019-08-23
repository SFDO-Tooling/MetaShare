import pytest
from channels.testing import WebsocketCommunicator

from ..api.push import report_error
from ..consumers import PushNotificationConsumer


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_push_notification_consumer__report_error(user_factory):
    user = user_factory()

    communicator = WebsocketCommunicator(PushNotificationConsumer, "/ws/notifications/")
    communicator.scope["user"] = user
    connected, _ = await communicator.connect()
    assert connected

    await communicator.send_json_to(
        {"model": "user", "id": str(user.id), "action": "SUBSCRIBE"}
    )
    response = await communicator.receive_json_from()
    assert "ok" in response

    await report_error(user)
    response = await communicator.receive_json_from()
    assert response == {
        "type": "BACKEND_ERROR",
        "payload": {"message": "There was an error"},
    }

    await communicator.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_push_notification_consumer__unsubscribe(user_factory):
    user = user_factory()

    communicator = WebsocketCommunicator(PushNotificationConsumer, "/ws/notifications/")
    communicator.scope["user"] = user
    connected, _ = await communicator.connect()
    assert connected

    await communicator.send_json_to(
        {"model": "user", "id": str(user.id), "action": "SUBSCRIBE"}
    )
    response = await communicator.receive_json_from()
    assert "ok" in response

    await communicator.send_json_to(
        {"model": "user", "id": str(user.id), "action": "UNSUBSCRIBE"}
    )
    response = await communicator.receive_json_from()
    assert "ok" in response

    await communicator.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_push_notification_consumer__invalid_subscription(user_factory):
    user = user_factory()

    communicator = WebsocketCommunicator(PushNotificationConsumer, "/ws/notifications/")
    communicator.scope["user"] = user
    connected, _ = await communicator.connect()
    assert connected

    await communicator.send_json_to({"model": "foobar", "id": "buzbaz"})
    response = await communicator.receive_json_from()
    assert "error" in response

    await communicator.disconnect()
