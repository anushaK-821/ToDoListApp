<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.sql.*" %>
<%
    if (session.getAttribute("username") == null) {
        response.sendRedirect("login.jsp");
    }
    int id = Integer.parseInt(request.getParameter("id"));
    Connection con = null;
    PreparedStatement ps = null;
    ResultSet rs = null;
    String title = null;
    String description = null;
    try {
        con = DBConnection.getConnection();
        String sql = "SELECT title, description FROM tasks WHERE id = ?";
        ps = con.prepareStatement(sql);
        ps.setInt(1, id);
        rs = ps.executeQuery();
        if (rs.next()) {
            title = rs.getString("title");
            description = rs.getString("description");
        } else {
            out.println("Task not found");
            return;
        }
    } catch (SQLException e) {
        e.printStackTrace();
    } finally {
        try { if (rs != null) rs.close(); } catch (SQLException e) {}
        try { if (ps != null) ps.close(); } catch (SQLException e) {}
        try { if (con != null) con.close(); } catch (SQLException e) {}
    }
%>
<html>
<head>
    <title>View Task</title>
</head>
<body>
    <h2>Task Details</h2>
    <p><b>ID:</b> <%=id%></p>
    <p><b>Title:</b> <%=title%></p>
    <p><b>Description:</b> <%=description%></p>
    <a href="index.jsp">Back to List</a>
</body>
</html>