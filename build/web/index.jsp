<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.sql.*" %>
<%
    if (session.getAttribute("username") == null) {
        response.sendRedirect("login.jsp");
    }
%>
<html>
<head>
    <title>To-Do List</title>
</head>
<body>
    <h2>Welcome, <%= session.getAttribute("username") %></h2>
    <a href="LogoutServlet">Logout</a><br><br>
    <a href="add.jsp">Add New Task</a><br><br>
    <h3>Task List:</h3>
    <%
        Connection con = null;
        Statement st = null;
        ResultSet rs = null;
        try {
            con = DBConnection.getConnection();
            st = con.createStatement();
            String sql = "SELECT id, title, description FROM tasks";
            rs = st.executeQuery(sql);
            while (rs.next()) {
                int id = rs.getInt("id");
                String title = rs.getString("title");
                String description = rs.getString("description");
                out.println("<p>");
                out.println("ID: " + id + "<br>");
                out.println("Title: " + title + "<br>");
                out.println("Description: " + description + "<br>");
                out.println("<a href='edit.jsp?id=" + id + "'>Edit</a> | ");
                out.println("<a href='DeleteTaskServlet?id=" + id + "'>Delete</a>");
                out.println("</p><br>");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            try { if (rs != null) rs.close(); } catch (SQLException e) {}
            try { if (st != null) st.close(); } catch (SQLException e) {}
            try { if (con != null) con.close(); } catch (SQLException e) {}
        }
    %>
</body>
</html>