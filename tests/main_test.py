from app.main import Post


# Create Post instance with all required fields (title, content)
def test_create_post_with_required_fields():
    post = Post(title="Test Title", content="Test Content")
    assert post.title == "Test Title"
    assert post.content == "Test Content"
    assert post.published is True
    assert post.rating is None


# Create Post instance with all fields including optional ones
def test_create_post_with_all_fields():
    post = Post(title="Test Title", content="Test Content", published=False, rating=5)
    assert post.title == "Test Title"
    assert post.content == "Test Content"
    assert post.published is False
    assert post.rating == 5


# Create Post with empty strings for title and content
def test_create_post_with_empty_strings():
    post = Post(title="", content="")
    assert post.title == ""
    assert post.content == ""
    assert post.published is True
    assert post.rating is None
