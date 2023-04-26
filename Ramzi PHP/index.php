<?php 

$host="localhost";      # host name or ip address 
$user="root";           # database user name
$pass="root";    		# database password
$database="ramzi_db";	# dateabase name with which you want to connect


$conn = new mysqli($host, $user, $pass, $database);
if($conn->connect_error){
    die("Ошибка: " . $conn->connect_error);
}
echo "<p style='background-color: #00fb00'>Подключение успешно установлено</p>";


if ($_POST) {
/*     echo '<pre>';
    echo htmlspecialchars(print_r($_POST, true));
    echo '</pre>'; */

	if($_POST["action_"] == 1){
		if($_POST["objName"] != ""){
			if($_POST["actionType"] == "I"){
				
				$sql = "INSERT INTO dishes (name) VALUES ('" . $_POST["objName"] . "')";
				if($conn->query($sql)){
					echo "<p style='background-color: #00fb00'>Блюдо успешно добавлено</p>";
				} else{
					echo "<p style='background-color: #ff5656'>Ошибка: " . $conn->error . "</p>";
				}
			}
			else{
			
				$sql = "DELETE FROM dishes WHERE `dishes`.`name` = '" . $_POST["objName"] . "';";
				if($conn->query($sql)){
					echo "<p style='background-color: #00fb00'>Блюдо успешно удалено</p>";
				} else{
					echo "<p style='background-color: #ff5656'>Ошибка: " . $conn->error . "</p>";
				}
			}
		}
		else{
			echo "<p style='background-color: #ff5656'>Ошибка доабвления блюда: поле наименвоания пустое!</p>";
		}
	}
	elseif($_POST["action_"] == 2){
		if($_POST["objName"] != ""){
			if($_POST["actionType"] == "I"){
				
				$sql = "INSERT INTO ingredients (name) VALUES ('" . $_POST["objName"] . "')";
				if($conn->query($sql)){
					echo "<p style='background-color: #00fb00'>Ингридиент успешно добавлен</p>";
				} else{
					echo "<p style='background-color: #ff5656'>Ошибка: " . $conn->error . "</p>";
				}
			}
			else{
				$sql = "DELETE FROM ingredients WHERE ingredients.name = '" . $_POST["objName"] . "';";
				if($conn->query($sql)){
					echo "<p style='background-color: #00fb00'>Ингридиент успешно удалено</p>";
				} else{
					echo "<p style='background-color: #ff5656'>Ошибка: " . $conn->error . "</p>";
				}
			}
		}
		else{
			echo "<p style='background-color: #ff5656'>Ошибка доабвления ингридиента: поле наименвоания пустое!</p>";
		}

	}
	elseif($_POST["action_"] == 3){
		if($_POST["objName"] != "" && $_POST["textAr"] != ""){
			if($_POST["actionType"] == "I"){
				
				$list = explode(";",$_POST["textAr"]);
				$sql = "CREATE TEMPORARY TABLE `TT_Ingr` SELECT id FROM `ingredients` WHERE name in ('";

				foreach($list as $ingr){
					$sql = $sql . $ingr . "', '";
				}
				$sql = $sql . " ')
				;";
				$conn->query($sql);

				$sql = "SELECT 
				dishes.id as dishes_id, TT_Ingr.id as ingredients_id FROM dishes INNER JOIN TT_Ingr on dishes.name = '" . $_POST["objName"] . "';";
				echo $sql;
				if($result = $conn->query($sql)){

					foreach($result as $res){
						$sql = "INSERT INTO dishes_ingredients (id_dishes, id_ingredients) VALUES (" . $res["dishes_id"] . "," . $res["ingredients_id"] . ");";
						if(!$conn->query($sql)){
							echo "<p style='background-color: #ff5656'>2 Ошибка: " . $conn->error . "</p>";
							break;
						}
					}
					echo "<p style='background-color: #00fb00'>Список ингридиентов успешно добавлен</p>";
				} else{
					echo "<p style='background-color: #ff5656'>1 Ошибка: " . $conn->error . "</p>";
				}
			}
			else{

			}
		}
		else{
			echo "<p style='background-color: #ff5656'>Ошибка доабвления списка ингридиентов: поле наименвоания или дополнительное поле пустое!</p>";
		}
	}

}



?>


<!DOCTYPE html>
<html>
<head>
	<title>Ramzi Admin php</title>
    <link rel="stylesheet" type="text/css" href="myStyle.css">
	<meta charset="UTF-8">
</head>
<body>
	<form action="index.php" method="post">
		<p>Выбериет действие:</p>
		<ol>
			<li><input type="radio" name="action_" value="1" checked>Блюдо</li>
			<li><input type="radio" name="action_" value="2">Ингридиент</li>
			<li><input type="radio" name="action_" value="3">Ингридиенты в блюдах (запишите ингридиенты в дополнительном поле через ";")</li>
		</ol>

		<p>Выберите тип действие:</p>
		<input type="radio" name="actionType" value="I" checked>Добавить
		<input type="radio" name="actionType" value="D">Удалить

		<p>Запишите название блюда или ингридиента:</p>
		<input type="text" name="objName" style="width: 50%;">
		<p>Дополнительное поле:</p>
		<textarea name="textAr" style="width: 50%;"></textarea>
		<p></p>
		<input type="submit">
		<a href="index.php">Сбросить</a>
	</form>

	<div style="width: 24%; height: 60ch;display: inline-block;" >
		<p>Таблица блюд:</p>
		<table border="1" style="width: 100%;">
			<tbody>
				<tr style="background-color: rgb(197, 197, 197);">
					<td>№</td>
					<td>Название блюда</td>
				</tr>
                <?php 
                $sql = "SELECT name FROM dishes";
                $i = 1;
                if($result = $conn->query($sql)){
                    foreach($result as $row){
                        echo "<tr><td>";
                        echo $i;
                        echo "</td><td>";

                        $i = $i + 1;

                        echo $row["name"];
                        echo "</td></tr>";
                    }
                }
                
                
                ?>
<!-- 				<tr>
					<td>100</td>
					<td>Яичница</td>
				</tr> -->
			</tbody>
		</table>
	</div>
	<div style="width: 24%; height: 60ch; display: inline-block;">
		<p>Таблица ингридиентов:</p>
		<table border="1" style="width: 100%;">
			<tbody>
				<tr style="background-color: rgb(197, 197, 197);">
					<td>№</td>
					<td>Название ингридиента</td>
				</tr>
                <?php 
                $sql = "SELECT name FROM ingredients";
                $i = 1;
                if($result = $conn->query($sql)){
                    foreach($result as $row){
                        echo "<tr><td>";
                        echo $i;
                        echo "</td><td>";

                        $i = $i + 1;

                        echo $row["name"];
                        echo "</td></tr>";
                    }
                }
                
                
                ?>
			</tbody>
		</table>
	</div>
	<div style="width: 49%; height: 60ch; display: inline-block;">
		<p>Таблица ингридиентов в блюдах:</p>
		<table border="1" style="width: 100%;">
			<tbody>
				<tr style="background-color: rgb(197, 197, 197);">
					<td>№</td>
					<td>Название блюда</td>
					<td>Перечисление ингридиентов</td>
				</tr>
                <?php 
                $sql = "
                SELECT dishes_ingredients.id_dishes AS dishes_id, dishes.name AS dishes_name, ingredients.name AS ingredients_name FROM `dishes_ingredients` 
                INNER JOIN `ingredients` ON ingredients.id = dishes_ingredients.id_ingredients 
                INNER JOIN `dishes` ON dishes.id = dishes_ingredients.id_dishes order by dishes_ingredients.id_dishes;
                ";
                $i = 1;
                $last_dishes_id = -1;
                if($result = $conn->query($sql)){
                    foreach($result as $row){
                        if ($last_dishes_id == -1){
                            $last_dishes_id = $row["dishes_id"];

                            echo "<tr><td>";
                            echo $i;
                            echo "</td><td>";

                            echo $row["dishes_name"];
                            echo "</td>";

                            echo "<td><ol>";
                        }
                        elseif ($last_dishes_id != $row["dishes_id"]){
                            $last_dishes_id = $row["dishes_id"];
                            $i = $i + 1;
                            echo "</ol></td></tr>";

                            echo "<tr><td>";
                            echo $i;
                            echo "</td><td>";
                            
                            echo $row["dishes_name"];
                            echo "</td>";

                            echo "<td><ol>";
                        }

                        echo "<li>";
                        echo $row["ingredients_name"];
                        echo "</li>";


                    }
                } 
                
                
                ?>
			<!-- 	<tr>
					<td>1</td>
					<td>Яичница</td>
					<td>
						<ol>
							<li>Яйца</li>
							<li>Вода</li>
							<li>Сахар</li>
						</ol>
					</td>
				</tr> -->
			</tbody>
		</table>
	</div>
</body>
</html>

<?php $conn->close(); ?>