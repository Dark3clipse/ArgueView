from ToastApi import ToastApi
from ToastApi.Axiom import Axiom
from ToastApi.Premise import Premise
from ToastApi.Assumption import Assumption
from ToastApi.KnowledgePreference import KnowledgePreference
from ToastApi.RegularRule import RegularRule
from ToastApi.Contrariness import Contrariness
from ToastApi.RulePreference import RulePreference
from ToastApi.Consequent import Consequent
from Dataset import Dataset
from typing import List
import json
import http.server
import socketserver
import webbrowser


class Dialogue:

    _dataset: Dataset
    _case: int

    _addressee: str
    _source: str
    _domain: str
    _proposition: str

    _scheme: List[str]
    _conclusion: str

    def __init__(self, dataset: Dataset, case: int):

        # fill properties
        self._dataset = dataset
        self._case = case
        self._addressee = input('What is your name?\n')
        self._source = "bank_manager"
        self._domain = "loan_applications"
        self._accuracy = "{:.2f}".format(self._dataset.accuracy())

        self._proposition = "applicable"
        if self._dataset.y_pred[self._case] == 1:
            self._proposition = "not_"+self._proposition

        toast = ToastApi()

        P1 = Premise("expert", [self._source, self._domain])
        P2 = Premise("in_domain", [self._proposition, self._domain])
        P3 = Premise("asserts", [self._source, self._proposition])
        P4 = Premise("accurate", [self._source])
        P5 = Premise("complete", [self._addressee])

        probable = Consequent("probable", ['p']).A(['p'])
        probableX = Consequent("probable", ['X'])
        conclusionPositive = Consequent("conclusion", ['a'])
        conclusionNegative = Consequent("~conclusion", ['a'])
        notExpert = Consequent("~expert", ['X', self._domain])
        notComplete = Consequent("~complete", [self._addressee])
        expertX = Premise("expert", ['X', self._domain])

        exception = Premise("exception", [self._proposition])
        fraud = Premise("fraud", [self._source])
        fraud_aged = Premise("fraud_aged", [self._source])
        notFraud = Premise("~fraud", [self._source])

        R1 = RegularRule("R1", [P1.A([self._source, self._domain]), P2.A(['X', self._domain]), P3.A([self._source, 'X']), P4.A([self._source]), P5.A([self._addressee])], probableX, defeasible=True)
        R2 = RegularRule("R2", [probableX], conclusionPositive, defeasible=True)
        R3 = RegularRule("R3", [exception], conclusionNegative, defeasible=True)
        R4 = RegularRule("R4", [fraud], notExpert.A(['X', self._domain]), defeasible=True)
        R5 = RegularRule("R5", [fraud], notComplete.A([self._addressee]), defeasible=True)
        R6 = RegularRule("R6", [exception], notComplete.A([self._addressee]), defeasible=True)
        R7 = RegularRule("R6", [fraud_aged], notFraud, defeasible=True)

        RP1 = RulePreference("RP1", R3, R2)
        RP2 = RulePreference("RP2", R4, R1)
        RP3 = RulePreference("RP3", R7, R4)
        RP4 = RulePreference("RP4", R7, R5)

        KP1 = KnowledgePreference("KP", notFraud, fraud)

        # add user critique here
        toast.setAxioms([])

        self._scheme = []
        self._scheme.append(P1.compile().replace(" ", ""))
        self._scheme.append(P2.compile().replace(" ", ""))
        self._scheme.append(P3.compile().replace(" ", ""))
        self._scheme.append(P4.compile().replace(" ", ""))
        self._scheme.append(P5.compile().replace(" ", ""))
        self._scheme.append(probable.compile().replace(" ", ""))
        self._conclusion = "conclusion("+self._proposition+")"

        toast.setPremises([P1, P2, P3, P4, P5])
        toast.setAssumptions([fraud])
        toast.setPreferences([KP1])
        toast.setRules([R1, R2, R3, R4, R5, R6, R7])
        toast.setRulePreferences([RP1, RP2, RP3, RP4])
        toast.setContrarinesses([])

        #eval = toast.evaluate("conclusion("+self._proposition+")")
        eval = toast.evaluate("expert(bank_manager, loan_applications)")
        self.parseResult(eval)

    def parseResultArgument(self, arg: str):

        spl3 = arg.split(sep=": ")
        arg_nr = spl3[0]
        arg = spl3[1]

        spl = arg.split(sep="=>")
        arg_not = False
        if len(spl) == 2:
            arg_from = spl[0]
            spl2 = spl[1].split(sep="~")
            if len(spl2) == 2:
                arg_not = True
                arg_to = spl2[1]
            else:
                arg_to = spl[1]
        else:
            arg_from=""
            spl2 = arg.split(sep="~")
            if len(spl2) == 2:
                arg_not = True
                arg_to = spl2[1]
            else:
                arg_to = arg

        spl = arg_from.split(sep=",")
        arg_from = []
        for i in range(len(spl)):
            if len(spl[i]) > 0:
                arg_from.append(spl[i])

        return arg_nr, arg_from, arg_to, arg_not

    def testWithResult(self, loads, query: str):
        for i in range(len(loads["acceptableConclusions"]["0"])):
            v = loads["acceptableConclusions"]["0"][i]
            arg_not = False
            spl2 = v.split(sep="~")
            if len(spl2) == 2:
                arg_not = True
                v = spl2[1]

            q_not = False
            spl2 = query.split(sep="~")
            if len(spl2) == 2:
                q_not = True
                query = spl2[1]

            if (query == v) & (arg_not == q_not):
                return True
        return False

    indd = []
    def getItemIndex(self, loads, item: str) -> int:

        spl2 = item.split(sep="~")
        if len(spl2) == 2:
            item = spl2[1]

        for i in range(len(self.indd)):
            if self.indd[i] == item:
                return i
        self.indd.append(item)
        return len(self.indd)-1

    def lgc(self, loads, item):
        for i in range(len(loads["acceptableConclusions"]["0"])):
            v = loads["acceptableConclusions"]["0"][i]
            spl2 = v.split(sep="~")
            if len(spl2) == 2:
                v = spl2[1]

            if item == v:
                return i

        startindex = len(loads["acceptableConclusions"]["0"])
        for i in range(len(loads["arguments"])):
            arg_nr, arg_from, arg_to, arg_not = self.parseResultArgument(loads["arguments"][i])
            if item == arg_to:
                return startindex+i

        return -1

    def parseResult(self, eval: str):
        loads = json.loads(eval)
        print(json.dumps(loads, indent=4, sort_keys=True))

        # generate a network plot

        NODE_ITEM = 1
        NODE_SCHEME = 2
        NODE_CONCLUSION = 3

        nodes = []
        links = []
        for i in range(len(loads["arguments"])+10):
            nodes.append({})
        for i in range(len(loads["arguments"])):
            arg_nr, arg_from, arg_to, arg_not = self.parseResultArgument(loads["arguments"][i])

            argnr = int(arg_nr.split(sep="A")[1])-1
            nodenr = self.getItemIndex(loads, arg_to)

            res = self.testWithResult(loads, arg_to)

            for i in range(len(arg_from)):

                for j in range(len(loads["arguments"])):
                    jarg_nr, jarg_from, jarg_to, jarg_not = self.parseResultArgument(loads["arguments"][j])
                    if jarg_nr == arg_from[i]:
                        source_node = self.getItemIndex(loads, jarg_to)
                        break
                #fromnr = int(arg_from[i].split(sep="A")[1]) - 1
                obj = {"source": source_node, "target": nodenr, "value": 1}
                links.append(obj)



            if arg_to in self._scheme:
                type = NODE_SCHEME
            elif arg_to == self._conclusion:
                type = NODE_CONCLUSION
            else:
                type = NODE_ITEM

            obj = {"name": arg_to, "group": type, "state": (1 if res else 0)}

            nodes[nodenr] = obj

        while {} in nodes:
            nodes.remove({})


        # write to json
        json_data = {"nodes": nodes, "links": links}
        filename_out = 'assets/network.json'
        json_out = open(filename_out, 'w')
        json_out.write(json.dumps(json_data, indent=1, sort_keys=True))
        json_out.close()

        # start server
        PORT = 8000
        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("serving at port", PORT)
            webbrowser.open("http://localhost:8000/assets/network.html")
            httpd.serve_forever()

    def exampleToast(self) -> None:
        toast = ToastApi()

        snores = Premise("snores", ['bob'])
        professor = Premise("professor", ['bob'])

        p1 = KnowledgePreference("p1", professor, snores)

        misbehaves = Consequent("misbehaves")
        accessDenied = Consequent("accessDenied")
        accessAllowed = Consequent("accessAllowed")

        r1 = RegularRule("r1", [snores], misbehaves, defeasible=True)
        r2 = RegularRule("r2", [misbehaves], accessDenied, defeasible=True)
        r3 = RegularRule("r3", [professor], accessAllowed, defeasible=True)

        rp1 = RulePreference("rp1", r2, r1)
        rp2 = RulePreference("rp2", r3, r1)
        rp3 = RulePreference("rp3", r3, r2)

        c1 = Contrariness("c1", accessDenied, accessAllowed)

        toast.setAxioms([])
        toast.setPremises([snores, professor])
        toast.setAssumptions([])
        toast.setPreferences([p1])
        toast.setRules([r1, r2, r3])
        toast.setRulePreferences([rp1, rp2, rp3])
        toast.setContrarinesses([c1])

        print(toast.evaluate())