# Lilee T-Cloud Fullstack Engineer Assignment

| Author: Preston Tseng

## Getting Started

Step 1. Run Docker Compose

```
$ docker compose up
```

Step 2. Access the frontend page: [http://localhost:3000](http://localhost:3000)

## Functionality

### Create A Vehicle

1. Click on the “Add a Vehicle” button in the top left corner.

   ![1713012960388](image/README/1713012960388.png)
2. Enter the name of the vehicle and click “Submit”.

   ![1713012995126](image/README/1713012995126.png)
3. You can see the added vehicle in the table.

   ![1713013039611](image/README/1713013039611.png)

### Update The Name Of Vehicle

1. Find the row of the vehicle you want to update and click on the pencil button.
   ![1713013071557](image/README/1713013071557.png)
2. Update the name of the vehicle in the input field and then click “Submit”. If you decide not to update, please click “Cancel”.

   ![1713013112600](image/README/1713013112600.png)
3. After clicking "Submit", you can see the updated name of the vehicle in the table.

   ![1713013254464](image/README/1713013254464.png)

### Delete A Vehicle

1. Find the row of the vehicle you want to delete and click on the trash can button.

   ![1713013282551](image/README/1713013282551.png)
2. In the confirmation dialog, click “Yes”. If you decide not to delete, please click “No”.

   ![1713013328633](image/README/1713013328633.png)
3. After clicking "Yes", the vehicle has been deleted.

   ![1713013357594](image/README/1713013357594.png)

### Real-Time Vehicle Speed Simulation

1. In the row of the vehicle you want to monitor the speed of, click the play button. After clicking, the button will be replaced with a stop button.

   ![1713013413701](image/README/1713013413701.png)
2. In the speed column, the vehicle’s speed will be updated at a frequency of 1Hz.

   ![1713013437755](image/README/1713013437755.png)
3. If you want to stop monitoring, please click the stop button. After clicking, the speed field will stop updating.

   ![1713013459976](image/README/1713013459976.png)
