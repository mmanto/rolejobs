"use strict";

/**
 * Job detail controller
 * @memberof Jobs
 * @ngdoc controller
 * @name JobDetailCtl
 */

const factory = function ($scope, $state, $sce, $mdDialog, AlertModal, jobData, Apiv1Service) {

    const POSTULATION_STATUS = "postulation_status";

    console.log("Detail", jobData);
    $scope.jobData = jobData;

    $scope.postulationStatus = {
        0x00: {
            type: "info",
            message: "Estás postulado a este aviso," + 
                     " aún está en espera de respuesta"
        },
        0x10: {
            type: "success",
            message: "Han aceptado tu postulación a este aviso"
        },
        0x20: {
            type: "alert",
            message: "Tu postulación a este aviso ha sido rechazada"
        }
    };

    $scope.getDescription = (function () {
        var cache = null;

        return function (force = false) {
            if (!force && cache) {
                return cache;
            }

            cache = $sce.trustAsHtml($scope.jobData.description);

            return cache;
        };
    })();

    $scope.postulate = function () {
        if (jobData[POSTULATION_STATUS] !== null) {
            return AlertModal.open(
                "Ya tiene una postulación a este aviso."
            );
        }
        
        Apiv1Service.getInstance().get("accounts/postulationauthcheck")
            .then((response)=>{
                if (response.data.success){
                    $state.go("jobs.postulate", {
                        id: jobData.pk
                    });
                }
                else
                {
                    AlertModal.open("Primero debe registrarse antes de postularse.");
                    $state.go("accounts.signup");
                }
                

            });

            

    };

    $scope.enterpricejobsdialog = function (ev) {
        

        $mdDialog.show({
            controller: EnterpriceJobsDialogController,
            template: `
            
            <md-dialog>
  
        <md-toolbar>
        <div class="md-toolbar-tools" aria-label="Avisos relacionados">
            <h2 style="color: white">Avisos relacionados</h2>
            <span flex></span>
            
        </div>
        </md-toolbar>

    <md-dialog-content>


        <md-list>
            <md-list-item ng-repeat="job in enterpricejobs">
                <a ng-click="cancel()" ui-sref="jobs.detail({id: {{job.pk}} })">
                {{ job.title }} - {{ job.geo.city.name }}
                </a> 
            </md-list-item>
            <p ng-if="enterpricejobs.length == 0" style="margin:5px" > No se encontraron avisos relacionados </p>
        </md-list>
        
    </md-dialog-content>

    
  
</md-dialog>`,

            parent: angular.element(document.body),
            targetEvent: ev,
            clickOutsideToClose:true
          })

    };


    function EnterpriceJobsDialogController($scope, $mdDialog) {
    

        $scope.cancel = function() {
          $mdDialog.cancel();
        };

        Apiv1Service.getInstance().post("jobs/enterpricejobs",{ pk: jobData.pk })
            .then((response)=>{
                
                $scope.enterpricejobs = response.data;


            });
    
      }

};

module.exports = [
    "$scope",
    "$state",
    "$sce",
    "$mdDialog",
    "AlertModal",
    "jobData",
    "Apiv1Service",
    factory
];
