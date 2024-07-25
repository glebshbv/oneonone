from db.models.message_history import MessageHistory as MessageHistoryModel
from api.utils.message_history import get_message_history_by_user_id


def test_get_message_history_by_user_id(db_session):
    # Create a sample message history entry
    message = MessageHistoryModel(role="role", content="content", user_id=1)
    db_session.add(message)
    db_session.commit()

    # Test function
    result = get_message_history_by_user_id(db_session, 1)
    assert len(result) == 1
    assert result[0].role == "role"
    assert result[0].content == "content"
    assert result[0].user_id == 1