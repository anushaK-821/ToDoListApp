<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Add Task</title>
</head>
<body>
    <h2>Add New Task</h2>
    <form action="AddTaskServlet" method="post">
        Task Title: <input type="text" name="title" required><br><br>
        Task Description: <input type="text" name="description" required><br><br>
        <input type="submit" value="Add Task">
    </form>
    <a href="index.jsp">Back to List</a>
</body>
</html>