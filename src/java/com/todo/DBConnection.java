import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DBConnection {
    private static Connection con;

    public static Connection getConnection() {
        if (con == null) {
            try {
                // Class.forName("com.mysql.jdbc.Driver"); // For older versions
                Class.forName("com.mysql.cj.jdbc.Driver"); // For MySQL Connector/J 8.0+
                con = DriverManager.getConnection(
                        "jdbc:mysql://localhost:3306/tododb", // Replace with your database URL
                        "root", // Replace with your database username
                        ""); // Replace with your database password
            } catch (ClassNotFoundException | SQLException e) {
                e.printStackTrace();
            }
        }
        return con;
    }
}