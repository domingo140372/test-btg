SELECT 
	CONCAT(cli.nombres,", ", cli.apellidos) as cliente,
	prod.nombre as producto,
	suc.nombre as sucursal 
FROM
	clientes as cli
		INNER JOIN inscripciones as ins ON ins.id_cliente = cli.id
		INNER JOIN productos as prod ON prod.id = ins.id_producto
		INNER JOIN disponibilidades as disp ON disp.id_producto = prod.id
		INNER JOIN sucursales as suc ON suc.id = disp.id_sucursal
		INNER JOIN visitantes as vis ON vis.id_cliente = cli.id and vis.id_sucursal = suc.id;
